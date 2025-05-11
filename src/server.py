import http.server
import ssl
import argparse
import os
import logging
import json
import urllib.parse
import urllib.request
import time

API_KEY =os.environ.get("API_KEY", "fallback-if-not-set")

WEATHER_API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

CACHE = {}
CACHE_TTL = 300  # seconds

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            data = json.loads(body)
            city = data.get("city", "London,UK")
        except (json.JSONDecodeError, TypeError):
            self._send_json_response(400, {"error": "Invalid JSON format or payload."})
            return

        encoded_city = urllib.parse.quote(city)

        if self.path == "/api/weather":
            api_url = f"{WEATHER_API_URL}/{encoded_city}?unitGroup=metric&include=current&key={API_KEY}"
        elif self.path == "/api/forecast":
            api_url = f"{WEATHER_API_URL}/{encoded_city}?unitGroup=metric&include=days&key={API_KEY}"
        else:
            self._send_json_response(404, {"error": "Endpoint not found"})
            return

        cache_key = (self.path, city)
        now = time.time()

        if cache_key in CACHE:
            cached = CACHE[cache_key]
            if now - cached["timestamp"] < CACHE_TTL:
                logging.info(f"Serving from cache: {cache_key}")
                self._send_json_response(200, json.loads(cached["data"]))
                return

        logging.info("Sleeping 0.5s to avoid API flood...")
        time.sleep(0.5)

        try:
            with urllib.request.urlopen(api_url) as response:
                weather_data = response.read()
                CACHE[cache_key] = {"timestamp": now, "data": weather_data}
                self._send_raw_json(200, weather_data)
        except Exception as e:
            logging.error(f"API error: {e}")
            self._send_json_response(500, {"error": "Error fetching weather data"})

    def _send_json_response(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def _send_raw_json(self, code, raw_bytes):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(raw_bytes)

    def log_message(self, format, *args):
        logging.info("%s - - %s", self.client_address[0], format % args)

def run_server(port, use_https=False):
    server_address = ("0.0.0.0", port)
    httpd = http.server.HTTPServer(server_address, MyHandler)

    if use_https:
        cert_file = os.environ.get("CERT_FILE", "certificates/wethercenter.crt")
        key_file = os.environ.get("KEY_FILE", "certificates/wethercenter.key")
        if os.path.exists(cert_file) and os.path.exists(key_file):
            logging.info("Starting server in HTTPS mode...")
            httpd.socket = ssl.wrap_socket(httpd.socket, keyfile=key_file, certfile=cert_file, server_side=True)
        else:
            logging.error("Certificate or key file not found. Running in HTTP mode.")

    logging.info(f"Server started on port {port} ({'HTTPS' if use_https else 'HTTP'})")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
        httpd.server_close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Python Web Server")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 80)))
    parser.add_argument("--https", action="store_true")
    args = parser.parse_args()

    run_server(args.port, args.https)
