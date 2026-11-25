#!/usr/bin/env python3
"""
Launcher for Capstone Project Interactive Dashboard
Opens the web dashboard in your default browser.
"""

import os
import sys
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

PORT = 8085
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def open_browser():
    url = f"http://localhost:{PORT}/dashboard.html"
    print(f"\n=======================================================")
    print(f" Capstone Project Interactive Dashboard Live!")
    print(f" URL: {url}")
    print(f" Press Ctrl+C in terminal to stop server.")
    print(f"=======================================================\n")
    webbrowser.open(url)

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', PORT), Handler)
    threading.Timer(0.8, open_browser).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard server.")
        server.server_close()
