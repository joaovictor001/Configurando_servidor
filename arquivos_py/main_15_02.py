
from http.server import SimpleHTTPRequestHandler
import os
import socketserver
from urllib.parse import urlparse,parse_qs


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
        elif self.path == '/login_failed':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(os.getcwd(),'login.html'),"r", encoding="utf-8") as login_file:
                content = login_file.read()
                
            mensagem = "Login e/ou senha incorreta. Tente novamente."
            content = content.replace('<!-- Mensagem de erro sera inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
            
            self.wfile.write(content.encode('utf-8'))
            
        elif self.path.startswith('/cadastro'):
            
            query_params = parse_qs(urlparse(self.path).query)
            login = query_params.get('login',[''][0])
            senha = query_params.get('senha',[''][0])
            
            welcome_mensage = f"Olá {login}, seja bem-vindo! Parecemos que voce é novo por aqui. Complete o seu cadastro"
            
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r', encoding='utf-8') as cadastro_file:
                content = cadastro_file.read()
                
            content = content.replace('{login}', login)
            content = content.replace('{senha}', senha)
            content = content.replace('{welcome_mensage}', welcome_mensage)
            
            self.wfile.write(content.encode('utf-8'))
            
            return
            
             
            
        else:
            super().do_GET()
            
        
        
            
    def usuario_exsitente(self, login ,senha):
        with open ("dados_login.txt" , 'r', encoding="utf-8") as file:
            for line in file:
                stored_login, stored_senha = line.strip("").split(";")
                if login == stored_login:
                    print("Cheguei aqui significando que localizei o login")
                    print("senha: "+senha)
                    print("senha_armazenada: "+senha)
                    
                    return senha == stored_senha
        return False 
    
    def remover_ultima_linha(self,arquivo):
        print("vou excluir ultima linha")
        with open(arquivo,'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(arquivo, 'w', encoding= 'utf-8') as file:
            file.writelines(lines[:-1])             

    def do_POST(self):
        if self.path == '/enviar_login':

            content_length = int(self.headers['content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body, keep_blank_values=True)
            print("DADOS DO FORMULÁRIO")
            print("E-mail:", form_data.get('email', [''][0]))
            print("Senha:", form_data.get('senha', [''][0]))
            
            login = form_data.get('email',[''])[0]
            senha = form_data.get('senha',[''])[0]
            
            if self.usuario_exsitente(login,senha):
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                mensagem = f"Usuario {login} Logado com sucesso!!!! "
                self.wfile.write(mensagem.encode('utf-8'))
            else:
                if any(line.startswith(f"{login};") for line in open ("dados_login.txt",'r', encoding="utf-8")):
                    self.send_response(302)
                    self.send_header('location', '/login_failed')
                    self.end_headers()
                    return
                else:
                
                    with open('dados_login.txt','a', encoding='utf-8') as file:
                        senha = form_data.get('senha', [''])[0]
                        file.write(f"{login};{senha}\n")
                        
                    with open(os.path.join(os.getcwd(), 'cadastrado.html'), 'r') as accept_page:
                        content = accept_page.read()

                    self.send_response(302)
                    self.send_header("Content-type", f"/cadastro?login={login}$senha={senha}")
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                    
        elif self.path.startswith('/confirmar_cadastro'):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body,keep_blank_values=True)
            
            login = form_data.get('login',[''])[0]
            senha = form_data.get('senha',[''])[0]
            nome = form_data.get('nome',[''])[0]
            
            print("Nome: "+nome)
        else:
            super(MyHandler,self).do_POST()
        


        
endereco_ip="0.0.0.0"
porta = 8000

with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciado em {endereco_ip}:{porta}")
    httpd.serve_forever()
    
    