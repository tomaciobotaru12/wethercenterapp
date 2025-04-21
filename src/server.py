import http.server
import ssl
import argparse
import os
import logging
import json
import urllib.parse
import urllib.request

# === CONFIG ===
API_KEY = "GZ89HBFLCJ8XLT7R8HEQJSTKK"
WEATHER_API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        city = data.get("city", "London,UK")
        encoded_city = urllib.parse.quote(city)

        if self.path == "/api/weather":
            api_url = f"{WEATHER_API_URL}/{encoded_city}?unitGroup=metric&include=current&key={API_KEY}"
        elif self.path == "/api/forecast":
            api_url = f"{WEATHER_API_URL}/{encoded_city}?unitGroup=metric&include=days&key={API_KEY}"
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        try:
            with urllib.request.urlopen(api_url) as response:
                weather_data = response.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(weather_data)
        except Exception as e:
            logging.error(f"API error: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error fetching weather data")

    def log_message(self, format, *args):
        logging.info("%s - - %s", self.client_address[0], format % args)

def run_server(port, use_https=False):
    server_address = ("0.0.0.0", port)
    httpd = http.server.HTTPServer(server_address, MyHandler)

    if use_https:
        cert_file = os.environ.get("CERT_FILE", "certificates/wethercenter.crt")
        key_file = os.environ.get("KEY_FILE", "certificates/wethercenter.key")

        if not (os.path.exists(cert_file) and os.path.exists(key_file)):
            logging.error("Certificate or key file not found! Running in HTTP mode instead.")
        else:
            logging.info("Starting server in HTTPS mode...")
            httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=key_file, certfile=cert_file, server_side=True)

    logging.info(f"Server started on port {port} ({'HTTPS' if use_https else 'HTTP'})")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python Web Server")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 80)), help="Port to run the server on")
    parser.add_argument("--https", action="store_true", help="Enable HTTPS mode")
    args = parser.parse_args()

    run_server(args.port, args.https)
