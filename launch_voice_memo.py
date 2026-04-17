"""Launch the Voice Memo browser app with a local HTTP server.

This script is designed for users who prefer double-clicking a file:
- starts a local static server
- opens the app URL in the default browser
- keeps the terminal open with clear messages
"""

from __future__ import annotations

import http.server
import socketserver
import threading
import webbrowser
from pathlib import Path

HOST = "127.0.0.1"
PORT = 8000
APP_FILE = "index.html"


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    app_path = repo_root / APP_FILE

    if not app_path.exists():
        print(f"Error: {APP_FILE} was not found next to this launcher.")
        input("Press Enter to close...")
        return 1

    handler = http.server.SimpleHTTPRequestHandler

    try:
        with ReusableTCPServer((HOST, PORT), handler) as httpd:
            url = f"http://{HOST}:{PORT}/{APP_FILE}"
            print("Voice Memo app is starting...")
            print(f"Open this URL if your browser does not open automatically: {url}")
            print("Press Ctrl+C to stop the server.")

            threading.Timer(0.6, lambda: webbrowser.open(url)).start()
            httpd.serve_forever()
    except OSError as exc:
        print(f"Could not start local server on {HOST}:{PORT}.\n{exc}")
        print("Tip: close any app already using port 8000, then run again.")
        input("Press Enter to close...")
        return 1
    except KeyboardInterrupt:
        print("\nServer stopped.")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
