from http.server import BaseHTTPRequestHandler, HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Case 1: Success (200 OK)
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Welcome! Server is running.</h1>")

        # Case 2: Simulated Error (500 Internal Server Error)
        elif self.path == '/error':
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"500: Something went wrong internally!")

        # Case 3: Not Found (404 Not Found)
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404: Page not found.")

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8081), MyServer)
    print("Server started http://localhost:8081")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()