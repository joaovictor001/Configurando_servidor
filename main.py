
import os

from http.server import SimpleHTTPRequestHandler

import socketserver
from urllib.parse import parse_qs, urlparse
import hashlib
from database import conectar

conexao = conectar()

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
            
    # def usuario_existente(self, login, senha):
    #     #verifica se o login já existe
    #         with open('dados.login.txt', 'r', encoding='utf-8') as file:
    #             for line in file:
    #                 if line.strip():
    #                     stored_login, stored_senha_hash, stored_nome = line.strip().split(';')
    #                 if login == stored_login:
    #                     senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
    #                     print("Cheguei aqui significando que localizei o login informado.")
    #                     print("senha:" + senha)
    #                     print("senha_armazenada:" + senha)
    #                     print(stored_senha_hash)
    #                     return senha_hash == stored_senha_hash
    #         return False
    def usuario_existente(self, login, senha):
        print(login+"_"+senha)
        cursor = conexao.cursor()
        cursor.execute("SELECT senha FROM dados_login WHERE login = %s",(login,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            senha_hash = hashlib.sha256(senha.encode('utf-8')).hexdigest()
            return senha_hash == resultado[0]
        
        return False    
    
    
    # def Turma_existente(self, codigo, descricao):
    #     #verifica se o login já existe
    #         with open('dados.turmas.txt', 'r', encoding='utf-8') as file:
    #             for line in file:
    #                 if line.strip():
    #                     codigo_txt,descricao_txt = line.strip().split(';')
    #                 if codigo == codigo_txt:
    #                     print(descricao)
    #                     print(descricao_txt)
    #                     return codigo == codigo_txt
    #         return False
    
    
    def Turma_existente(self,Desc):
        cursor = conexao.cursor()
        cursor.execute("SELECT descricao FROM turmas WHERE descricao = %s",(Desc,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return True
        else:
            return False
    def Atividade_existente(self,Desc):
        cursor = conexao.cursor()
        cursor.execute("SELECT descricao FROM atividades WHERE descricao = %s",(Desc,))
        resultado = cursor.fetchone()
        cursor.close()
        if resultado:
            return True
        else:
            return False
        
         
        
    # def Atividade_existente(self, codigo, descricao):
    #     #verifica se o login já existe
    #         with open('dados.aitividade.txt', 'r', encoding='utf-8') as file:
    #             for line in file:
    #                 if line.strip():
    #                     codigo_txt,descricao_txt = line.strip().split(';')
    #                 if codigo == codigo_txt:
    #                     print(descricao)
    #                     print(descricao_txt)
    #                     return codigo == codigo_txt
    #         return False
   
    # def adicionar_usuario(self,login,senha,nome):
    #     senha_hash = hashlib.sha256(senha.encode("UTF-8")).hexdigest()
    #     with open('dados.login.txt', 'a', encoding='UTF-8') as file:
    #         file.write(f'{login};{senha_hash};{nome}\n')
    def adicionar_usuario(self,login,senha,nome):
        cursor = conexao.cursor()
        senha_hash = hashlib.sha256(senha.encode("UTF-8")).hexdigest()
        cursor.execute("INSERT INTO dados_login(login,senha,nome) VALUES (%s,%s, %s) ", (login,senha_hash,nome))
        
        conexao.commit()
        
        cursor.close()
        
    def adicionar_turma(self,Desc):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO turmas(descricao) VALUES (%s) ",(Desc,))
        
        conexao.commit()
        
        cursor.close()
        
    
            
    # def adicionar_turma(self,turma,descricao):
    #     with open('dados.turmas.txt', 'a', encoding='UTF-8') as file:
    #         file.write(f'{turma};{descricao}\n')
            
    def adicionar_atividade(self,Desc):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO atividades(descricao) VALUES (%s) ",(Desc,))
        
        conexao.commit()
        
        cursor.close()
        
    def remover_ultima_linha(self,arquivo):
        print("Vou excluir ultima linha")
        with open(arquivo, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            with open(arquivo, 'w', encoding='utf-8') as file:
                file.writelines(lines[:-1])
                
    def adicionar_turma_professor(self, descTurma,id_professor):
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO turmas (descricao) VALUES (%s)", (descTurma,))
        cursor.execute("SELECT id_turma FROM turmas WHERE descricao = %s ",(descTurma,))
        resultado = cursor.fetchone()
        cursor.execute("INSERT INTO turmas_professor (id_TURMA, id_professor) VALUES (%s, %s)",(resultado[0], id_professor))
        conexao.commit()
        cursor.close()

    def carregar_turmas_professor(self,login):
        print("!!!!!cheguei aqui !!!!!"+ login)
        cursor =conexao.cursor()
        cursor.execute("SELECT id_professor, nome FROM dados_login WHERE login = %s",(login,))
        resultado = cursor.fetchone()
        cursor.close()

        id_professor = resultado[0]

        cursor = conexao.cursor()
        cursor.execute(
            "SELECT turmas.id_turma, turmas.descricao FROM turmas_professor INNER JOIN turmas "
            "ON turmas_professor.id_turma  = turmas.id_turma WHERE turmas_professor.id_professor = %s",(id_professor,))
        turmas = cursor.fetchall()
        cursor.close()

        linhas_tabela = ""
        for turma in turmas:
            id_turma = turma[0]
            descricao_turma = turma[1]
            link_atividade = "<img src='icnatividade2.png'/>"
            linhas = "<tr><td style='text-aling:center'>{}</td><td style='text-aling:center'>{}</td></tr>".format(descricao_turma,link_atividade)
            linhas_tabela += linhas

        with open (os.path.join(os.getcwd(), 'Sistema Educacional/Cadastro de Turma.html'),'r',encoding='utf-8') as cad_turma_file:
            content = cad_turma_file.read()

            content = content.replace('{nome_professor}',resultado[1])
            content = content.replace('{id_professor}', str(id_professor))
            content = content.replace('{login}',str(login))

        content = content.replace('<!-- Tabela com linha zebradas -->', linhas_tabela)
        self.send_response(200)
        self.send_header("content-type", "text/html; charset=utf-8")
        self.end_headers()


        self.wfile.write(content.encode('utf-8'))
 
    def do_POST(self):

        if self.path == '/enviar_login':
            print("cheguei aqui")
 
            content_length = int(self.headers['content-Length'])

            body = self.rfile.read(content_length).decode('utf-8')
          
            form_data = parse_qs(body)
 
            print(form_data)
            print("DADOS DO FORMULÁRIO")
            print("E-mail:", form_data.get('email',[''])[0])
            print("Senha:", form_data.get('senha',[''])[0])
           
            login = form_data.get('email',[''])[0]
            senha = form_data.get('senha',[''])[0]
            print("TESTE DE VALOR: "+ login,senha)
           
            if self.usuario_existente(login, senha):
                print(login+"AQUI")
                self.carregar_turmas_professor(login)
            else:
                cursor = conexao.cursor()
                cursor.execute("SELECT login FROM dados_login WHERE login = %s",(login,))
                resultado = cursor.fetchone()
                
                
                if resultado:
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    cursor.close()
                    return
                    
    
                else:
                    # self.adicionar_usuario(login,senha, nome='None')
                    self.send_response(302)
                    self.send_header('Location', f'novo_cadastro?login={login}&senha={senha}')
                    self.end_headers()
                    cursor.close()
                    return
        
        elif self.path.startswith('/confirmar_cadastro'):
         
            content_length = int(self.headers['Content-Length'])
       
            body= self.rfile.read(content_length).decode('utf-8')
   
            from_data = parse_qs(body, keep_blank_values=True)
 
            login = from_data.get('email', [''])[0]
            senha = from_data.get('senha', [''])[0]
            nome = from_data.get('nome', [''])[0]
 
            
            self.adicionar_usuario(login, senha,nome)
            self.send_response(302)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("registro recebido com sucesso !". encode('utf-8'))
                    
        elif self.path.startswith('/cad_turmas'):
            content_length = int(self.headers['Content-Length'])
            #le o corpo dA REQUISIÇÃO
            body= self.rfile.read(content_length).decode('utf-8')
            #Parseia os dados do formulario
            form_data = parse_qs(body, keep_blank_values=True)
 
            Descricao = form_data.get('Descricao',[''])[0]
            id_professor = form_data.get('id_professor',[''])[0]
            login = form_data.get('login',[''])[0]


            print(f"Cad_turma, dados do formulario {Descricao}{id_professor}")
            self.adicionar_turma_professor(Descricao,id_professor)
            self.carregar_turmas_professor(login)
            
            if self.Turma_existente(Descricao):
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
                self.adicionar_turma_professor(Descricao,id_professor)
                with open(os.path.join(os.getcwd(), 'Sistema Educacional/Cadastro de Turma.html'), 'r',encoding='UTF-8') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("content-type","text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))  
                  
        elif self.path.startswith('/cad_atividade'):
            content_length = int(self.headers['Content-Length'])
    
            body= self.rfile.read(content_length).decode('utf-8')
         
            from_data = parse_qs(body, keep_blank_values=True)
 
            
            Descricao = from_data.get('Descricao', [''])[0]
            
            if self.Atividade_existente(Descricao):
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
                self.adicionar_atividade(Descricao)
                self.send_response(302)
                with open(os.path.join(os.getcwd(), 'Sistema Educacional/Tela Professor.html'), 'r', encoding='utf-8') as existe:
                    content_file = existe.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content_file.encode('utf-8'))
                  
                
        else:
            super(MyMandler,self).do_POST()
            
endereco_ip = "0.0.0.0"
porta = 8000
with socketserver.TCPServer((endereco_ip, porta), MyMandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    httpd.serve_forever()