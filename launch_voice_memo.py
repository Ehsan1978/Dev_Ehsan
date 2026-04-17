"""Launch the Voice Memo browser app with a local HTTP server."""

from __future__ import annotations

import contextlib
import http.server
import os
import socket
import socketserver
import threading
import time
import webbrowser
from pathlib import Path

HOST = "127.0.0.1"
PREFERRED_PORT = 8000
APP_FILE = "index.html"


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def find_free_port(start: int = PREFERRED_PORT, attempts: int = 20) -> int:
    for port in range(start, start + attempts):
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if sock.connect_ex((HOST, port)) != 0:
                return port
    raise OSError(f"No free ports found in range {start}-{start + attempts - 1}.")


def try_open_browser(url: str) -> None:
    def _open() -> None:
        try:
            webbrowser.open(url, new=2)
        except Exception:
            pass

    threading.Thread(target=_open, daemon=True).start()


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    app_path = repo_root / APP_FILE

    if not app_path.exists():
        print(f"Error: {APP_FILE} was not found next to this launcher.")
        input("Press Enter to close...")
        return 1

    os.chdir(repo_root)

    try:
        port = find_free_port()
        with ReusableTCPServer((HOST, port), http.server.SimpleHTTPRequestHandler) as httpd:
            url = f"http://{HOST}:{port}/{APP_FILE}"

            print("Voice Memo app server is running.")
            print(f"Open this URL in your browser: {url}")
            print("The browser should open automatically in a moment.")
            print("Press Ctrl+C to stop the server.")

            time.sleep(0.3)
            try_open_browser(url)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        return 0
    except OSError as exc:
        print(f"Could not start local server.\n{exc}")
        input("Press Enter to close...")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
