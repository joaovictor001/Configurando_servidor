
import os 
from http.server import SimpleHTTPRequestHandler

import socketserver
from urllib.parse import parse_qs,urlparse
import hashlib


class MyMandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f =  open(os.path.join(path,"index.html"),"r")
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            
            self.wfile(f.read().encode('utf-8'))
            
            f.close
            return None
        except FileNotFoundError:
            pass
        
        return super().list_directory(path)
    
    def do_GET(self):
            if self.path =='/login':

                try:
                    with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login_file:
                        content = login_file.read()
                    self.send_response(200)
                    self.send_header("content-type","text/html")
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))          

                except FileNotFoundError:
                    pass
    
endereco_ip = "0.0.0.0"
porta = 8000
 

with socketserver.TCPServer((endereco_ip, porta), MyMandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    httpd.serve_forever()