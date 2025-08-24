import http.server
import socketserver
import webbrowser
import threading
import os
import socket

FILENAME = "qr_password_vault.html"
START_PORT = 8080
MAX_TRIES = 20

class LoggableHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Redirect root path to FILENAME
        if self.path == "/" or self.path == "":
            self.send_response(302)
            self.send_header("Location", f"/{FILENAME}")
            self.end_headers()
            return
        else:
            super().do_GET()
    def do_POST(self):
        if self.path == "/log":
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length)
            print("[WEB LOG]", data.decode(errors="ignore"))
            self.send_response(204)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # erişim loglarını görmek istemezsen alttakini aç ve üsttekini kapat
        # return
        super().log_message(format, *args)

def find_free_port(start=START_PORT, max_tries=MAX_TRIES):
    for port in range(start, start + max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    raise OSError("No free port found in range")

def start_server(port):
    handler = LoggableHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.exists(FILENAME):
        print(f"Hata: {FILENAME} bu klasörde bulunamadı.")
        exit(1)

    port = find_free_port()

    t = threading.Thread(target=start_server, args=(port,), daemon=True)
    t.start()

    url = f"http://localhost:{port}/{FILENAME}"
    print(f"Açılıyor: {url}")
    webbrowser.open(url)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nSunucu kapatılıyor...")