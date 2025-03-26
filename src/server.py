import http.server
import ssl
import argparse
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Welcome to WeatherCenter</h1><p>Your server is running!</p>")

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
