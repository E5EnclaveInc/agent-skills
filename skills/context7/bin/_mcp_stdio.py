"""Vendored stdio MCP client core (mcp Python SDK 1.x API).

One tool call per process: spawn server, initialize, call tool, print JSON, exit.
Security properties:
  - argv is hardcoded by the calling skill; shell is never used.
  - child env is scrubbed (PATH/HOME/LANG only, plus skill-supplied extras).
  - output is byte-capped to stop context-bomb DoS on the calling agent.
  - a hard timeout kills the call; the stdio context manager tears down the child.
"""
import asyncio
import json
import os
import sys

MAX_OUTPUT_BYTES = 200_000


def scrubbed_env(extra=None):
    env = {
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "HOME": os.environ.get("HOME", "/root"),
        "LANG": "C.UTF-8",
        "PYTHONIOENCODING": "utf-8",
    }
    # Sandbox MITMs TLS with a custom CA (paths, not secrets) — without these,
    # every TLS connection from an MCP server fails verification.
    for var in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "NODE_EXTRA_CA_CERTS",
                "GIT_SSL_CAINFO", "CURL_CA_BUNDLE", "AWS_CA_BUNDLE",
                "NODE_USE_ENV_PROXY"):
        if var in os.environ:
            env[var] = os.environ[var]
    if extra:
        env.update(extra)
    return env


async def _call(command, args, tool, params, timeout, env, cwd):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    sp = StdioServerParameters(command=command, args=list(args), env=env, cwd=cwd)
    async with stdio_client(sp) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return await session.call_tool(tool, params or {})


def call_tool(command, args, tool, params=None, timeout=120, extra_env=None, cwd=None):
    """Call one MCP tool. Returns dict(output, truncated, is_error)."""
    env = scrubbed_env(extra_env)
    try:
        result = asyncio.run(
            asyncio.wait_for(_call(command, args, tool, params, timeout, env, cwd),
                             timeout + 15)
        )
    except asyncio.TimeoutError:
        raise RuntimeError("tool call timed out; server process torn down")
    texts = []
    for block in (result.content or []):
        t = getattr(block, "text", None)
        if t is not None:
            texts.append(t)
        else:
            texts.append("[non-text content block omitted]")
    out = "\n".join(texts)
    truncated = False
    raw = out.encode("utf-8")
    if len(raw) > MAX_OUTPUT_BYTES:
        out = raw[:MAX_OUTPUT_BYTES].decode("utf-8", "replace") + "\n[TRUNCATED]"
        truncated = True
    return {
        "output": out,
        "truncated": truncated,
        "is_error": bool(getattr(result, "isError", False)),
    }


async def _list_tools(command, args, timeout, env, cwd):
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    sp = StdioServerParameters(command=command, args=list(args), env=env, cwd=cwd)
    async with stdio_client(sp) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            return [{"name": t.name, "description": t.description} for t in tools.tools]


def list_tools(command, args, timeout=120, extra_env=None, cwd=None):
    env = scrubbed_env(extra_env)
    return asyncio.run(
        asyncio.wait_for(_list_tools(command, args, timeout, env, cwd), timeout + 15)
    )


if __name__ == "__main__":
    # Smoke helper: python _mcp_stdio.py list-tools '<json argv>'
    if len(sys.argv) == 3 and sys.argv[1] == "list-tools":
        argv = json.loads(sys.argv[2])
        print(json.dumps(list_tools(argv[0], argv[1:], extra_env=json.loads(os.environ.get("MCP_EXTRA_ENV", "{}"))), indent=2))
    else:
        sys.exit("usage: _mcp_stdio.py list-tools '<json argv>'")
