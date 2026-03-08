"""
One-time Notion OAuth setup. Run this, click Allow in the browser, done.
"""
import base64
import http.server
import json
import os
import ssl
import subprocess
import sys
import tempfile
import threading
import urllib.parse
import urllib.request
import webbrowser

CLIENT_ID     = os.environ.get("NOTION_OAUTH_CLIENT_ID", "31dd872b-594c-817a-8197-00378688f0cd")
CLIENT_SECRET = os.environ.get("NOTION_OAUTH_CLIENT_SECRET", "NOTION_OAUTH_SECRET_REDACTED")
REDIRECT_URI  = "https://localhost:3000/callback"
AUTH_URL      = (
    f"https://api.notion.com/v1/oauth/authorize"
    f"?client_id={CLIENT_ID}&response_type=code&owner=user"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}"
)
ENV_FILE = os.path.join(os.path.dirname(__file__), ".env")

received_code  = None
server_ready   = threading.Event()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global received_code
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        print(f"Got request: {self.path}", flush=True)
        if "code" in params:
            received_code = params["code"][0]
            body = b"<h1>Connected! You can close this tab.</h1>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            # Signal server to stop
            threading.Thread(target=self.server.shutdown).start()
        else:
            body = b"<h1>Waiting...</h1>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, *_):
        pass


def make_cert():
    """Generate a temporary self-signed cert for localhost."""
    d = tempfile.mkdtemp()
    cert = os.path.join(d, "cert.pem")
    key  = os.path.join(d, "key.pem")
    subprocess.run([
        "openssl", "req", "-x509", "-newkey", "rsa:2048",
        "-keyout", key, "-out", cert,
        "-days", "1", "-nodes",
        "-subj", "/CN=localhost",
    ], capture_output=True, check=True)
    return cert, key


def exchange_code(code):
    creds = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    payload = json.dumps({
        "grant_type":   "authorization_code",
        "code":         code,
        "redirect_uri": REDIRECT_URI,
    }).encode()
    req = urllib.request.Request(
        "https://api.notion.com/v1/oauth/token",
        data=payload,
        headers={
            "Authorization": f"Basic {creds}",
            "Content-Type":  "application/json",
        },
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx) as resp:
        return json.loads(resp.read())


def save_token(token):
    lines = []
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, encoding="utf-8") as f:
            lines = f.read().splitlines()
    found = False
    new_lines = []
    for line in lines:
        if line.startswith("NOTION_API_KEY="):
            new_lines.append(f"NOTION_API_KEY={token}")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"NOTION_API_KEY={token}")
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")
    os.environ["NOTION_API_KEY"] = token


def run():
    print("Generating SSL certificate for localhost...")
    try:
        cert, key = make_cert()
    except Exception as e:
        print(f"openssl not found ({e}). Trying fallback...")
        # Fallback: just print the URL and ask user to paste the code
        print("\nOpen this URL in your browser:")
        print(AUTH_URL)
        code = input("\nAfter clicking Allow, paste the 'code=' value from the redirect URL: ").strip()
        if not code:
            print("No code entered. Exiting.")
            sys.exit(1)
        do_exchange(code)
        return

    httpd = http.server.HTTPServer(("localhost", 3000), Handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

    print("Starting local HTTPS server on port 3000...")
    print("Opening Notion authorization page in your browser...\n")
    threading.Timer(1.0, lambda: webbrowser.open(AUTH_URL)).start()

    print("Waiting for Notion to redirect back...", flush=True)
    httpd.serve_forever()  # keeps running until handler calls shutdown()

    if received_code:
        do_exchange(received_code)
    else:
        print("No authorization code received.")
        sys.exit(1)


def do_exchange(code):
    print("Exchanging code for access token...")
    try:
        data = exchange_code(code)
    except Exception as e:
        print(f"Token exchange failed: {e}")
        sys.exit(1)

    token = data.get("access_token", "")
    if not token:
        print(f"Unexpected response: {data}")
        sys.exit(1)

    workspace = data.get("workspace_name", "unknown")
    bot_id    = data.get("bot_id", "")

    save_token(token)
    print(f"\nSuccess! Connected to workspace: {workspace}")
    print(f"Bot ID: {bot_id}")
    print(f"Access token saved to .env as NOTION_API_KEY")
    print("\nNotion is ready. Restart the server to pick up the new token.")


if __name__ == "__main__":
    run()
