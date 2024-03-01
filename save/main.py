
import os

from http.server import SimpleHTTPRequestHandler

import socketserver
from urllib.parse import parse_qs, urlparse
import hashlib
 

class MyMandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        # Tenta o Código abaixo
        try:
            f = open(os.path.join(path, 'login.html'), 'r')
            self.send_response(200)

            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(f.read().encode('utf-8'))

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
           
        elif self.path == '/login_failed':

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
           
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
               

            mensagem = "Login e/ou senha incorreta. Tente novamente"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
           
            self.wfile.write(content.encode('utf-8'))
            
        elif self.path == '/Turma_existente':

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(os.getcwd(), 'Sistema Educacional/Cadastro de Turma.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
               

            mensagem = "Turma ja existe em nosso banco"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
            self.wfile.write(content.encode('utf-8'))    
       
        elif self.path.startswith('/novo_cadastro'):
 
            query_params = parse_qs(urlparse(self.path).query)
            login = query_params.get('login',[''])[0]
            senha = query_params.get('senha',[''])[0]
            welcome_message = f"Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui.Complete seu cadastro"
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
 
            #le o conteudo da pagina html
            with open(os.path.join(os.getcwd(), 'cadastro.html'),'r', encoding='utf-8') as novo_cadastro_file:
                content = novo_cadastro_file.read()
 
            content = content.replace('{login}', login)
            content = content.replace('{senha}', senha)
            content = content.replace('{welcome_message}',welcome_message)
            self.wfile.write(content.encode('utf-8'))
 
            return 
        elif self.path =='/Turmas':

            try:
                with open(os.path.join(os.getcwd(), 'Sistema Educacional/Cadastro de Turma.html'), 'r',encoding='UTF-8') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("content-type","text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))          

            except FileNotFoundError:
                pass
            
        elif self.path =='/Atividade':

            try:
                with open(os.path.join(os.getcwd(), 'Sistema Educacional/Cadastro de Atividade.html'), 'r',encoding='UTF-8') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("content-type","text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))          

            except FileNotFoundError:
                pass
       
        else:
            super().do_GET()
            
    def usuario_existente(self, login, senha):
        #verifica se o login já existe
            with open('dados.login.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        stored_login, stored_senha_hash, stored_nome = line.strip().split(';')
                    if login == stored_login:
                        senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
                        print("Cheguei aqui significando que localizei o login informado.")
                        print("senha:" + senha)
                        print("senha_armazenada:" + senha)
                        print(stored_senha_hash)
                        return senha_hash == stored_senha_hash
            return False
    def Turma_existente(self, codigo, descricao):
        #verifica se o login já existe
            with open('dados.turmas.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        codigo_txt,descricao_txt = line.strip().split(';')
                    if codigo == codigo_txt:
                        print(descricao)
                        print(descricao_txt)
                        return codigo == codigo_txt
            return False
    def Atividade_existente(self, codigo, descricao):
        #verifica se o login já existe
            with open('dados.aitividade.txt', 'r', encoding='utf-8') as file:
                for line in file:
                    if line.strip():
                        codigo_txt,descricao_txt = line.strip().split(';')
                    if codigo == codigo_txt:
                        print(descricao)
                        print(descricao_txt)
                        return codigo == codigo_txt
            return False
   
    def adicionar_usuario(self,login,senha,nome):
        senha_hash = hashlib.sha256(senha.encode("UTF-8")).hexdigest()
        with open('dados.login.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{login};{senha_hash};{nome}\n')
            
    def adicionar_turma(self,turma,descricao):
        with open('dados.turmas.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{turma};{descricao}\n')
            
    def adicionar_atividade(self,cod_atividade,descricao):
        with open('dados.aitividade.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{cod_atividade};{descricao}\n')        
 
    def remover_ultima_linha(self,arquivo):
        print("Vou excluir ultima linha")
        with open(arquivo, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            with open(arquivo, 'w', encoding='utf-8') as file:
                file.writelines(lines[:-1])
 
    def do_POST(self):

        if self.path == '/enviar_login':
 
            content_length = int(self.headers['content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')
          
            form_data = parse_qs(body)
 
            print(form_data)
            print("DADOS DO FORMULÁRIO")
            print("E-mail:", form_data.get('email', [''])[0])
            print("Senha:", form_data.get('senha', [''])[0])
           
            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]
           
            if self.usuario_existente(login, senha):
                with open(os.path.join(os.getcwd(), 'Sistema Educacional/Tela Professor.html'), 'r', encoding='utf-8') as existe:
                    content_file = existe.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
            
                self.wfile.write(content_file.encode('utf-8'))
           
            else:
                if any(line.startswith(f"{login};") for line in open("dados.login.txt", "r", encoding="UTF-8")):
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    return # adicionando um return para evitar a execução
    
                else:
                        self.adicionar_usuario(login,senha, nome='None')
                        self.send_response(302)
                        self.send_header('Location', f'novo_cadastro?login={login}&senha={senha}')
                        self.end_headers()
                return # adicionando um return para evitar a execução
 
        elif   self.path.startswith('/confirmar_cadastro'):
         
            content_length = int(self.headers['Content-Length'])
       
            body= self.rfile.read(content_length).decode('utf-8')
   
            from_data = parse_qs(body, keep_blank_values=True)
 
            login = from_data.get('email', [''])[0]
            senha = from_data.get('senha', [''])[0]
            nome = from_data.get('nome', [''])[0]
 
            senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
            print("nome:" + nome)
 
            if self.usuario_existente(login,senha):
 
                with open('dados.login.txt','r', encoding='utf-8') as file:
                    lines = file.readlines()
 
                with open('dados.login.txt','w', encoding='utf-8') as file:
                    for line in lines:
                        stored_login, stored_senha,stored_nome = line.strip().split(';')
                        if login == stored_login and senha_hash == stored_senha:
                            line = f"{login};{senha_hash};{nome} \n"
                        file.write(line)

                    self.send_response(302)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    
            else:
                    self.remover_ultima_linha('dados.login.txt')
                    self.send_response(302)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("A senha não confere.Retome o procedimento!". encode('utf-8'))
                    
        elif self.path.startswith('/cad_turmas'):
            content_length = int(self.headers['Content-Length'])
            #le o corpo dA REQUISIÇÃO
            body= self.rfile.read(content_length).decode('utf-8')
            #Parseia os dados do formulario
            from_data = parse_qs(body, keep_blank_values=True)
 
            Codigo = from_data.get('Codigo',[''])[0]
            Descricao = from_data.get('Descricao',[''])[0]
            
            if self.Turma_existente(Codigo,Descricao):
                with open(os.path.join(os.getcwd(), 'Sistema Educacional/Cadastro de Turma.html'), 'r', encoding='utf-8') as existe:
                    content_file = existe.read()
                mensagem = "Turma ja existe em nosso banco"
                content_file = content_file.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
           
                self.wfile.write(content_file.encode('utf-8'))
      
            else:            
                self.adicionar_turma(Codigo,Descricao)
                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                  
        elif self.path.startswith('/cad_atividade'):
            content_length = int(self.headers['Content-Length'])
    
            body= self.rfile.read(content_length).decode('utf-8')
         
            from_data = parse_qs(body, keep_blank_values=True)
 
            Codigo = from_data.get('Codigo', [''])[0]
            Descricao = from_data.get('Descricao', [''])[0]
            
            if self.Atividade_existente(Codigo,Descricao):
                with open(os.path.join(os.getcwd(), 'Sistema Educacional/Cadastro de Atividade.html'), 'r', encoding='utf-8') as existe:
                    content_file = existe.read()
                mensagem = "Atividade ja existe em nosso banco"
                content_file = content_file.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
           
                self.wfile.write(content_file.encode('utf-8'))
                
            else:            
                self.adicionar_atividade(Codigo,Descricao)
                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                
        else:
            super(MyMandler,self).do_POST()
            
endereco_ip = "0.0.0.0"
porta = 8000
with socketserver.TCPServer((endereco_ip, porta), MyMandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    httpd.serve_forever()