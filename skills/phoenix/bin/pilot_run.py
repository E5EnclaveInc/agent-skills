#!/usr/bin/env python3
"""pilot_run.py — scoped Phoenix observability pilot.

Proves the OTel -> Phoenix wiring end-to-end with a realistic multi-step
pipeline (canary + simulated sweep iteration), then verifies the traces
actually landed by querying Phoenix's API. Phoenix is started for the pilot
and stopped afterwards (see phoenix_ctl.py).

Scope honesty: this instruments a *scripted* pipeline, not the live agent
loops. True agent-loop span emission needs runtime hooks the fleet doesn't
expose yet — staged as NEXT in the install receipt.

Span redaction: every attribute value is scrubbed for secret-shaped content
before export (API keys, tokens, bearer values, long hex blobs).
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
VENV_PY = os.path.join(os.environ.get("PHOENIX_VENV", os.path.expanduser("~/.venvs/phoenix")), "bin", "python")
HOST, PORT = "127.0.0.1", 6006

SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password|bearer)\s*[:=]\s*\S+"),
    re.compile(r"\b[0-9a-fA-F]{32,}\b"),  # long hex blobs
    re.compile(r"sk-[A-Za-z0-9]{8,}"),
]


def redact(value):
    if not isinstance(value, str):
        return value
    red = value
    for pat in SECRET_PATTERNS:
        red = pat.sub("[REDACTED]", red)
    return red


def api_get(path):
    req = urllib.request.Request(f"http://{HOST}:{PORT}{path}")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def main():
    run_id = uuid.uuid4().hex[:12]
    print(f"pilot run_id={run_id}")

    # Localhost export must never go through the sandbox egress proxy.
    for var in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                "http_proxy", "https_proxy", "all_proxy"):
        os.environ.pop(var, None)

    # 1. Start Phoenix.
    subprocess.run([VENV_PY, os.path.join(HERE, "phoenix_ctl.py"), "start"],
                   check=True)

    # 2. Emit spans via OTel -> OTLP/HTTP on the Phoenix main port.
    # (OTLP/gRPC on :4317 is unusable from this sandbox: grpcio routes it
    # through the egress proxy regardless of env. OTLP/HTTP is equivalent.)
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter)

    provider = TracerProvider(
        resource=Resource.create({"service.name": "phoenix-pilot",
                                  "pilot.run_id": run_id}))
    provider.add_span_processor(BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://127.0.0.1:6006/v1/traces")))
    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("pilot")

    canary_trace_id = None
    with tracer.start_as_current_span(
            "pilot.canary",
            attributes={"pilot.run_id": redact(run_id),
                        "note": redact("canary; proves export works")}) as s:
        canary_trace_id = format(s.get_span_context().trace_id, "032x")
        with tracer.start_as_current_span(
                "sweep.iteration",
                attributes={"queue": redact("chief-of-staff QUEUE.md"),
                            "items": 3}) :
            for step in ("queue.read", "task.draft", "report.write"):
                with tracer.start_as_current_span(
                        step,
                        attributes={"step": redact(step),
                                    # Deliberately secret-shaped: must arrive redacted.
                                    "auth_note": redact("api_key=AKIAIOSFODNN7EXAMPLE")}):
                    time.sleep(0.2)
    provider.force_flush(timeout_millis=15000)
    print(f"canary trace_id={canary_trace_id}")
    time.sleep(5)  # let Phoenix ingest

    # 3. Verify traces landed via the project-scoped REST API.
    found = False
    redaction_ok = False
    traces_path = "/v1/projects/default/traces?limit=100&include_spans=true"
    try:
        blob = json.dumps(api_get(traces_path))
        if canary_trace_id in blob:
            found = True
            print(f"VERIFIED: canary trace present via {traces_path}")
        else:
            print(f"{traces_path}: reachable, canary not in first page")
    except Exception as e:  # noqa: BLE001 - pilot diagnostics
        print(f"{traces_path}: {e}")
    # Redaction check at span-attribute level: the raw fake key must be
    # absent while the [REDACTED] marker is present.
    spans_path = ("/v1/projects/default/spans/otlpv1"
                  f"?trace_id={canary_trace_id}&limit=50")
    try:
        blob = json.dumps(api_get(spans_path))
        if "AKIAIOSFODNN7EXAMPLE" in blob:
            print("REDACTION-FAIL: raw secret-shaped value visible in Phoenix")
        elif "[REDACTED]" in blob:
            redaction_ok = True
            print("redaction check: [REDACTED] marker stored, raw key absent")
        else:
            print("redaction check inconclusive: marker not found")
    except Exception as e:  # noqa: BLE001
        print(f"{spans_path}: {e}")

    # 4. Smoke the built-in MCP endpoint (Phoenix >= 19 path, not the
    #    maintenance-mode standalone package).
    mcp_ok = False
    try:
        payload = json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "pilot", "version": "1"}}}
        ).encode()
        req = urllib.request.Request(
            f"http://{HOST}:{PORT}/mcp", data=payload,
            headers={"Content-Type": "application/json",
                     "Accept": "application/json, text/event-stream"})
        with urllib.request.urlopen(req, timeout=15) as r:
            body = r.read().decode(errors="replace")
            mcp_ok = "result" in body or "capabilities" in body
            print(f"/mcp initialize -> HTTP {r.status}, ok={mcp_ok}")
    except Exception as e:  # noqa: BLE001
        print(f"/mcp smoke: {e}")

    # 5. Stop Phoenix (pilot-only runtime).
    subprocess.run([VENV_PY, os.path.join(HERE, "phoenix_ctl.py"), "stop"],
                   check=True)

    if found and redaction_ok and mcp_ok:
        print("PILOT-PASS: OTel export works, traces land redacted, /mcp live")
    else:
        print("PILOT-PARTIAL: found=%s redaction_ok=%s mcp_ok=%s"
              % (found, redaction_ok, mcp_ok))
        sys.exit(2)


if __name__ == "__main__":
    main()
