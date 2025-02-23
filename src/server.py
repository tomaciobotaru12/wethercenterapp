from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
from socketserver import ThreadingMixIn
import threading
import os
from string import Template

hostName = "0.0.0.0"
serverPort = 80

class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
      # curl http://<ServerIP>/index.html
      version="v1.0"
      if self.path == "/":
          # Respond with the file contents.
          page_body_item=""          
          if os.environ.get('POD_NMAE') is not None:
            print(version+" POD_NAME:"+os.environ.get('HOSTNAME'))
            page_body_item = version + " POD_NMAE: " +os.environ.get('POD_NMAE')
          elif os.environ.get('HOSTNAME') is not None:
            print(version +" HOSTNAME:"+os.environ.get('HOSTNAME'))
            page_body_item = version +" HOSTNAME: " +os.environ.get('HOSTNAME')
          else:
            page_body_item = version  

          print("page_body: "+page_body_item)
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          self.end_headers()
          with open('index.html', 'r') as htmlfile:
              for html_line in htmlfile.read().split('\n'):               
                self.wfile.write(bytes(html_line.replace('{{OBS}}', page_body_item), 'utf-8'))          
          
          #content = open('index.html', 'rb').read()
          #self.wfile.write(content)
          
          
      else:
          self.send_response(404)

      return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  """Handle requests in a separate thread."""

if __name__ == "__main__":
  webServer = ThreadedHTTPServer((hostName, serverPort), Handler)
  print("Server started http://%s:%s" % (hostName, serverPort))

  try:
      webServer.serve_forever()
  except KeyboardInterrupt:
      pass

  webServer.server_close()
  print("Server stopped.")