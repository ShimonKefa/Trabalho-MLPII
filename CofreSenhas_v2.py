from dataclasses import dataclass
import random
import string
import os as os

# este método executa a lógica da criação da senha automatica - parte: Pedro Manzoli de Oliveira
class Pswrd_Gen_Service:
    DEFAULT_LENGTH = 8
    MIN_LENGTH = 6
    MAX_LENGTH = 64
    CHAR_POOL = string.ascii_letters + string.digits + string.punctuation
    def gen_Pswrd(self, length):
        if length is None:
            length = self.DEFAULT_LENGTH

        elif length < self.MIN_LENGTH or length > self.MAX_LENGTH:
            length = self.DEFAULT_LENGTH
            print(f"tamanho inválido. minimo de caractéres esperados é: ({self.DEFAULT_LENGTH})")

        return ''.join(random.choice(self.CHAR_POOL) for _ in range(length))


class Pessoa:
    def __init__(self,nome: str):
        self.nome = nome
        
class Usuario(Pessoa):
    def __init__(self,nome: str,email: str):
        super().__init__(nome)
        self.email = email
        
@dataclass
class Categoria:
    nome:str

class Credencial(Usuario):
    def __init__(self,nome: str,email: str,site: str,senha,categoria:Categoria):
        super().__init__(nome,email)
        self.site = site
        self.senha = senha
        self.categoria = categoria

class Seguranca():
    def criptografar(self,senha):
        return senha[::-1]
        
    def descriptografar(self,senha):
        return senha[::-1]
        
class Encrypted(Credencial, Seguranca):
    def __init__(self,nome: str ,email: str,site: str,senha,categoria: Categoria):
        super().__init__(nome,email,site,senha,categoria)
        self.senha = self.criptografar(senha)
        
    def mostrar(self):
        return f"{self.nome} | {self.email} | {self.site} | {self.descriptografar(self.senha)} | {self.categoria.nome}"
        
    #Cofre é um struct dinâmico que armazena os objetos que compõem a senha gerada pelo usuário, bem como website, nome da pessoa que adicionou e entre outros.       
cofre = []

class BUFFER_LENGHT_PSWRD_ERROR(Exception):
    pass        
class ErroDeCofre(Exception):
    pass
class SenhaErro(ErroDeCofre):
    pass
class NadaEncontrado(ErroDeCofre):
    pass


def Adicionar():
    try:
        nome = input ("Digite seu nome:")
        site = input ("Digite o nome do site/app:")
        email = input ("Digite o email do site/app:")

        #Este método introduz a lógica para a criação da senha utilizando a lib random -- parte: Pedro Manzoli de Oliveira
        categ_op = input("Deseja gerar uma senha automatica? -> Expected: (S/N) ").strip()
        if categ_op == 'S' or categ_op == 's':
            gen = Pswrd_Gen_Service()            
            aux1 = input("digite o tamanho da senha ").strip()
            senha_length = int(aux1) if aux1.isdigit() else None
            senha = gen.gen_Pswrd(senha_length)
            print(f"senha gerada: {senha}")
        else:
            senha = input ("Digite a senha do site/app:")

        categ = input ("Digite a categoria do site/app:")
        
        if len(senha) < 4:
            raise SenhaErro("Senha muito curta!")
            
        categoria = Categoria(categ_op)
        
        c = Encrypted(nome,email,site,senha,categoria)
        cofre.append(c)
        
        print("Senha salva com sucesso")

        input("Pressione Enter para continuar...")
        
    except ErroDeCofre as e:
        print(f"ERRO! {e}")

    # a estrutura `raise` utiliza um método de tratamento de excessão que quando atende uma condição emite uma excessão configurada pelo programador
    # o `IF NOT` é uma estrutura condicional reservada que valida uma entrada e retorna um booleano como true ou false.
    # Essa função tem por finalidade Listar todas as senhas criadas dentro do array c. 
def Listar():
    try:
        if not cofre:
            raise NadaEncontrado("Cofre Vazio! Tente Novamente")
            
        for c in cofre:
            print(c.mostrar())

        input("Pressione Enter para continuar...")
            
    except ErroDeCofre as e:
        print(f"ERRO! {e}")
        
        #Essa função tem a finalidade de buscar a senha criada pela nome do Site que é utilizado como chave primária
def Buscar():
    try:
        site = input ("Digite o nome do site/app para buscar:")
        
        resultado = [c for c in cofre if c.site == site]
        
        if not resultado:
            raise NadaEncontrado("Nada encontrado")
        
        
        for c in resultado:
            if site == c.site:
                print(c.mostrar())

        input("Pressione Enter para continuar...")
                
    except ErroDeCofre as e:
        print(f"ERRO! {e}")    
        
        #Essa função tem a Finaliade de Deletar as senhas do cofre
def Deletar():
    try:
        site = input ("Digite o nome do site/app para deletar:")
        
        for c in cofre:
            if c.site == site:
                cofre.remove(c) # remove do cofre
                print("Deletado!")
            
        raise SenhaErro("Senha incorreta")
        
    except ErroDeCofre as e:
        print(f"ERRO! {e}") 

    #Essa função tem a finalidade de limpar o terminal quando é chamada
def ClearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')      


    #Função Menu -- Entrada inicial do usuário.
def Menu():
    while True:
        ClearTerminal() 

        print("===$COFRE DE SENHA$===")
        print("1- Adicionar")
        print("2- Listar")
        print("3- Buscar")
        print("4- Deletar")
        print("5- Sair")
        
        opcao = input("Selecione:")
        
        match opcao:
            case "1":
                Adicionar()
            case "2":
                Listar()
            case "3":
                Buscar()
            case "4":
                Deletar()
            case "5":
                print("Saindo do cofre...")
                break
            case _:
                print("ERRO! Opção invalida")
Menu()