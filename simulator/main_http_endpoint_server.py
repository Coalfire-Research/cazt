# © 2023 Coalfire
#
# Author: Rodney Beede

import argparse
import base64
import http.server
import ssl
import os
from pathlib import Path
import re

import modules.moggy_worker


# Useful for referencing external files
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def main(args):
    print(f"[INFO] Starting HTTP web engine endpoint server on port {args.port}...")
    
    http_daemon = http.server.HTTPServer(
        ("", args.port),  # All IPv6 or IPv4 interfaces
        FunctionHandoffHTTPRequestHandler
    )
       
    http_daemon.socket = ssl.wrap_socket(
        http_daemon.socket,
        keyfile = Path(SCRIPT_DIR, "x509", "server.key"),
        certfile = Path(SCRIPT_DIR, "x509", "server.crt"),
        server_side = True,
        ssl_version = ssl.PROTOCOL_TLS_SERVER  # version agnostic
    )
    
    http_daemon.serve_forever()
    
    print(f"[INFO] terminating...")


class FunctionHandoffHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"  # some newer API clients use HTTP/2, but this is sufficient

    def do_POST(self):
        print(f"[DEBUG] Connection from f{self.client_address}")
        print("=" * 30)
        
        print(self.requestline)
        print(self.headers, end="")  # self.headers object converts to string with trailing \r\n
        
        # we won't support chunked encoding, if needed in future maybe the cgi module could help
        content_length = self.headers.get('Content-Length', None)
        if content_length:
            content_length = int(content_length)
            request_content_body = self.rfile.read(content_length)
            
            print(request_content_body.decode("utf-8"))
            print("-" * 30)
            print()
        else:
            print(f"[ERROR] Missing request header Content-Length from f{self.client_address}")
            self.send_response(400, "sad-kitty")
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write("Request missing Content-Type HTTP header".encode("utf-8"))
            return


        handler_payload = dict()
        handler_payload["body"] = request_content_body.decode("utf-8")
        
        # Path could look like /uat/apiEndpointName or /prod/apiEndpointName or just /apiEndpointName
        # We only care about the end part
        handler_payload["resource"] = "/" + os.path.basename(self.path)
        
        handler_payload["identity"] = dict()
        
        # Parse out some identity information
        if "Authorization" in self.headers:
            val = self.headers.get("Authorization")
            
            if "Bearer" in val:
                base64_credential = val[len("Bearer "):]

                try:
                    decoded_credential = base64.b64decode(base64_credential).decode("utf-8")
                except:
                    decoded_credential = ""  # Handle invalid

                parts = decoded_credential.split("@", 1)
                
                if 2 == len(parts):
                    handler_payload["identity"]["username"] = parts[0]
                    handler_payload["identity"]["accountId"] = parts[1]
                else:
                    handler_payload["identity"]["username"] = parts[0]
                    handler_payload["identity"]["accountId"] = None
            else:
                # No known way to parse here
                print("[WARN] Could not find any known cloud-provider Authorization header value")
                handler_payload["identity"]["username"] = val
                handler_payload["identity"]["accountId"] = val
        else:
            print("[WARN] No Authorization header seen")

        
        worker_response = modules.moggy_worker.function_handler(handler_payload, self.headers)
        
        self.send_response(worker_response["statusCode"])
        for header in worker_response["headers"]:
            self.send_header(header, worker_response["headers"][header])
        self.send_header("Content-Length", len(worker_response["body"].encode("utf-8")))
        self.end_headers()

        self.wfile.write(worker_response["body"].encode("utf-8"))


    def log_request(self, code):
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="https://www.coalfire.com/")

    parser.add_argument("--port", help="port to listen on",
        type=int, default=8443, choices=range(1,65535), metavar="[1-65535]")

    args = parser.parse_args()

    main(args)
