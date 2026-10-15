#!/usr/bin/env python3
"""Upload files/dirs TO a Lambda instance via its JupyterLab contents API.

Usage:
  jup-put.py <instance-id> <local-path> <remote-path>

<remote-path> is RELATIVE to the Jupyter root (/home/ubuntu).
Binary-safe (base64). Never prints the API key or Jupyter token.
"""
import base64
import tempfile
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jcommon import jupyter  # noqa: E402

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def put_file(base: str, token: str, local: Path, remote: str):
    body = {
        "type": "file",
        "format": "base64",
        "content": base64.b64encode(local.read_bytes()).decode(),
    }
    tmp = Path(tempfile.gettempdir()) / f"jup-put-{local.name}.json"
    tmp.write_text(json.dumps(body))
    url = f"{base}/api/contents/{remote}?token={token}"
    last = None
    for i in range(6):
        p = subprocess.run(
            ["curl", "-s", "--max-time", "300", "-A", UA, "-X", "PUT", url,
             "-H", "Content-Type: application/json", "--data-binary", f"@{tmp}"],
            capture_output=True, text=True, timeout=330)
        if p.returncode == 0 and p.stdout.strip():
            try:
                j = json.loads(p.stdout)
                if j.get("path"):
                    print(f"uploaded {local} -> {j['path']} ({local.stat().st_size} bytes)")
                    tmp.unlink(missing_ok=True)
                    return
                last = f"no path in response: {p.stdout[:120]}"
            except json.JSONDecodeError as e:
                last = f"bad json: {e}"
        else:
            last = f"rc={p.returncode} stderr={p.stderr[:120]}"
        time.sleep(min(30, 2 ** i))
    tmp.unlink(missing_ok=True)
    raise RuntimeError(f"upload failed for {local}: {last}")


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit("usage: jup-put.py <instance-id> <local-path> <remote-path>")
    iid, local, remote = sys.argv[1], Path(sys.argv[2]), sys.argv[3].strip("/")
    base, token = jupyter(iid)
    if local.is_dir():
        for child in sorted(local.rglob("*")):
            if child.is_file():
                put_file(base, token, child, f"{remote}/{child.relative_to(local)}")
    else:
        put_file(base, token, local, remote)


if __name__ == "__main__":
    main()
