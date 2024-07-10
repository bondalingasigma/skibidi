from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import proccess

# Define a custom request handler that extends BaseHTTPRequestHandler
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.startswith('/submit'):
            parsed_url = urlparse(self.path)
            query = parse_qs(parsed_url.query)
            if 'inputText' in query:
                input_text = query['inputText'][0]
                output = proccess.process(input_text)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes(f'Jarvis: {output}', 'utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes('Missing input parameter', 'utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes('Not found', 'utf-8'))

def run_server(ip='127.0.0.1', port=8650):
    # Determine the directory where the script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    website_dir = os.path.join(base_dir, 'website')

    # Change the current working directory to 'website'
    os.chdir(website_dir)

    # Set up the HTTP server with the specified IP, port, and request handler
    server_address = (ip, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)

    # Print a message indicating where the server is running
    print(f"Server running at http://{ip}:{port}/")

    # Start the HTTP server and keep it running indefinitely
    httpd.serve_forever()

# Run the server
if __name__ == "__main__":
    run_server()
