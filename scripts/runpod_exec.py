"""
RunPod Remote Execution via Jupyter WebSocket API (stdlib only)

Executes shell commands on a RunPod pod through Jupyter's kernel WebSocket.
No pip dependencies — uses only Python standard library.

Usage:
    python scripts/runpod_exec.py <pod_id> "<command>"
    python scripts/runpod_exec.py to53z2zsxrtgp5 "hostname && nvidia-smi"

Requires:
    JUPYTER_TOKEN env var (default: "adc3k")
    Pod must run runpod/pytorch image with Jupyter enabled
"""

import hashlib
import http.client
import json
import os
import ssl
import struct
import sys
import time
import uuid


JUPYTER_TOKEN = os.environ.get("JUPYTER_TOKEN", "")
if not JUPYTER_TOKEN:
    print("ERROR: JUPYTER_TOKEN env var is required.", file=sys.stderr)
    sys.exit(1)


def _https(host: str, method: str, path: str, body: bytes | None = None) -> tuple[int, str]:
    ctx = ssl.create_default_context()
    conn = http.client.HTTPSConnection(host, context=ctx, timeout=15)
    headers = {"Content-Type": "application/json"}
    conn.request(method, path, body=body, headers=headers)
    resp = conn.getresponse()
    data = resp.read().decode()
    conn.close()
    return resp.status, data


def _ws_connect(host: str, path: str) -> ssl.SSLSocket:
    """Minimal WebSocket handshake using stdlib."""
    import socket
    ctx = ssl.create_default_context()
    raw = socket.create_connection((host, 443), timeout=30)
    sock = ctx.wrap_socket(raw, server_hostname=host)

    # WebSocket handshake
    key = hashlib.sha1(uuid.uuid4().bytes).digest()
    import base64
    ws_key = base64.b64encode(key[:16]).decode()

    handshake = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Upgrade: websocket\r\n"
        f"Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {ws_key}\r\n"
        f"Sec-WebSocket-Version: 13\r\n"
        f"\r\n"
    )
    sock.sendall(handshake.encode())

    # Read response headers
    response = b""
    while b"\r\n\r\n" not in response:
        response += sock.recv(4096)

    if b"101" not in response.split(b"\r\n")[0]:
        raise RuntimeError(f"WebSocket handshake failed: {response[:200].decode()}")

    return sock


def _ws_send(sock, message: str):
    """Send a WebSocket text frame (masked, as required by client)."""
    payload = message.encode("utf-8")
    # Frame: FIN=1, opcode=1 (text)
    frame = bytearray()
    frame.append(0x81)  # FIN + text

    length = len(payload)
    if length < 126:
        frame.append(0x80 | length)  # MASK bit set
    elif length < 65536:
        frame.append(0x80 | 126)
        frame.extend(struct.pack(">H", length))
    else:
        frame.append(0x80 | 127)
        frame.extend(struct.pack(">Q", length))

    # Masking key
    mask = os.urandom(4)
    frame.extend(mask)

    # Masked payload
    masked = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))
    frame.extend(masked)

    sock.sendall(bytes(frame))


def _ws_recv(sock, timeout: float = 30.0) -> str | None:
    """Receive a WebSocket text frame."""
    sock.settimeout(timeout)
    try:
        # Read frame header
        header = sock.recv(2)
        if len(header) < 2:
            return None

        opcode = header[0] & 0x0F
        masked = (header[1] & 0x80) != 0
        length = header[1] & 0x7F

        if length == 126:
            length = struct.unpack(">H", sock.recv(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", sock.recv(8))[0]

        if masked:
            mask = sock.recv(4)

        # Read payload
        data = b""
        while len(data) < length:
            chunk = sock.recv(length - len(data))
            if not chunk:
                break
            data += chunk

        if masked:
            data = bytearray(b ^ mask[i % 4] for i, b in enumerate(data))

        if opcode == 0x01:  # Text frame
            return data.decode("utf-8")
        elif opcode == 0x08:  # Close
            return None
        elif opcode == 0x09:  # Ping
            # Send pong
            pong = bytearray([0x8A, 0x80]) + os.urandom(4)
            sock.sendall(bytes(pong))
            return _ws_recv(sock, timeout)
        else:
            return _ws_recv(sock, timeout)  # Skip non-text frames

    except (TimeoutError, OSError):
        return None


def exec_on_pod(pod_id: str, command: str, timeout: int = 120) -> str:
    """Execute a shell command on a RunPod pod via Jupyter kernel WebSocket."""
    host = f"{pod_id}-8888.proxy.runpod.net"

    # Step 1: Create kernel
    status, body = _https(host, "POST", f"/api/kernels?token={JUPYTER_TOKEN}", b'{"name":"python3"}')
    if status >= 400:
        raise RuntimeError(f"Failed to create kernel: HTTP {status}: {body[:200]}")
    kernel = json.loads(body)
    kernel_id = kernel["id"]
    print(f"  Kernel: {kernel_id[:12]}...", file=sys.stderr)

    # Wait for kernel to be ready
    time.sleep(2)

    # Step 2: Connect WebSocket
    ws_path = f"/api/kernels/{kernel_id}/channels?token={JUPYTER_TOKEN}"
    print(f"  Connecting WebSocket...", file=sys.stderr)
    sock = _ws_connect(host, ws_path)
    print(f"  Connected.", file=sys.stderr)

    # Step 3: Send execute request
    msg_id = str(uuid.uuid4())
    session_id = str(uuid.uuid4())

    code = f"import subprocess, sys\nr = subprocess.run({command!r}, shell=True, capture_output=True, text=True, timeout={timeout - 10})\nprint(r.stdout, end='')\nif r.stderr:\n    print(r.stderr, end='', file=sys.stderr)\nprint(f'\\n__RC__={{r.returncode}}')"

    msg = json.dumps({
        "header": {
            "msg_id": msg_id,
            "msg_type": "execute_request",
            "username": "mc",
            "session": session_id,
            "date": time.strftime("%Y-%m-%dT%H:%M:%S.000000Z", time.gmtime()),
            "version": "5.3",
        },
        "parent_header": {},
        "metadata": {},
        "content": {
            "code": code,
            "silent": False,
            "store_history": False,
            "user_expressions": {},
            "allow_stdin": False,
            "stop_on_error": True,
        },
        "buffers": [],
        "channel": "shell",
    })

    _ws_send(sock, msg)
    print(f"  Executing: {command[:60]}...", file=sys.stderr)

    # Step 4: Collect output
    stdout_parts = []
    stderr_parts = []
    deadline = time.time() + timeout
    done = False

    while time.time() < deadline and not done:
        raw = _ws_recv(sock, timeout=5.0)
        if raw is None:
            continue

        try:
            response = json.loads(raw)
        except json.JSONDecodeError:
            continue

        parent_id = response.get("parent_header", {}).get("msg_id", "")
        if parent_id != msg_id:
            continue

        msg_type = response.get("msg_type", "")

        if msg_type == "stream":
            text = response["content"].get("text", "")
            name = response["content"].get("name", "stdout")
            if name == "stderr":
                stderr_parts.append(text)
            else:
                stdout_parts.append(text)

        elif msg_type == "error":
            tb = response["content"].get("traceback", [])
            stderr_parts.append("\n".join(tb))
            done = True

        elif msg_type == "execute_reply":
            done = True

    sock.close()

    output = "".join(stdout_parts)
    errors = "".join(stderr_parts)

    # Parse exit code
    lines = output.rstrip().split("\n")
    if lines and lines[-1].startswith("__RC__="):
        rc = int(lines[-1].split("=")[1])
        output = "\n".join(lines[:-1])
        if rc != 0:
            print(f"  [Exit code: {rc}]", file=sys.stderr)

    if errors:
        print(errors, file=sys.stderr)

    return output


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <pod_id> <command>")
        print(f'Example: python {sys.argv[0]} abc123xyz "hostname && nvidia-smi"')
        sys.exit(1)

    pod_id = sys.argv[1]
    command = " ".join(sys.argv[2:])  # Allow unquoted multi-word commands

    print(f"  Pod: {pod_id}", file=sys.stderr)
    print(f"  Cmd: {command}", file=sys.stderr)

    output = exec_on_pod(pod_id, command)
    sys.stdout.buffer.write(output.encode("utf-8", errors="replace"))
    sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
