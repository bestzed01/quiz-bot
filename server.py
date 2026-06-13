#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

PORT = int(os.environ.get("PORT", 8080))

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self.path = "/webapp.html"
        return super().do_GET()
    def log_message(self, *args): pass

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print(f"Serving on port {PORT}", flush=True)
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
