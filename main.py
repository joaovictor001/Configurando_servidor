
from http.server import SimpleHTTPRequestHandler
import os
import socketserver
from urllib.parse import parse_qs


# port = 8000
# handler = SimpleHTTPRequestHandler
# server = HTTPServer(('localhost',port),handler)

# print(f"Sevidor rodando em http://localhost:{port}")


# server.serve_forever()


class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path,'home.html'),'r')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileExistsError:
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
        # Caso dê erro
            except FileNotFoundError:
                pass
        else:
            super().do_GET()
            
    def usuario_exsitente(self, login):
        with open ("dados_login.txt" , 'r') as file:
            for line in file:
                stored_login, joao = line.strip("").split(";")
                if login == stored_login:
                    return True
        return False            

    def do_POST(self):
        if self.path == '/enviar_login':

            content_length = int(self.headers['content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)
            print("DADOS DO FORMULÁRIO")
            print("E-mail:", form_data.get('email', [''][0]))
            login = form_data.get('email',[''])[0]
            
            if self.usuario_exsitente(login):
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                mensagem = f"Usuario {login} ja consta em nossos registros"
                self.wfile.write(mensagem.encode('utf-8'))
            else:
                with open('dados_login.txt','a', encoding='utf-8') as file:
                    senha = form_data.get('senha', [''])[0]
                    file.write(f"{login};{senha}\n")
                    
                with open(os.path.join(os.getcwd(), 'cadastrado.html'), 'r') as accept_page:
                    content = accept_page.read()

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
        else:
            super(MyHandler,self).do_POST()


        
endereco_ip="0.0.0.0"
porta = 8000

with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciado em {endereco_ip}:{porta}")
    httpd.serve_forever()
    
    