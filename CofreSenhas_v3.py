# Importações necessárias
from dataclasses import dataclass  # Facilita criação de classes simples (tipo struct)
import random  # Para gerar números aleatórios
import string  # Contém conjuntos de caracteres (letras, números, etc)
import os      # Usado pra limpar o terminal


# Serviço responsável por gerar senhas aleatórias
class PswrdGenService:
    DEFAULT_LENGTH = 8   # Tamanho padrão da senha
    MIN_LENGTH = 6       # Tamanho mínimo permitido
    MAX_LENGTH = 64      # Tamanho máximo permitido

    # Conjunto de caracteres possíveis
    CHAR_POOL = string.ascii_letters + string.digits + string.punctuation

    # Método que gera senha
    def gen_Pswrd(self, length):
        if length is None:
            length = self.DEFAULT_LENGTH  # Usa padrão se não informado
        elif length < self.MIN_LENGTH or length > self.MAX_LENGTH:
            # Se tamanho inválido, volta pro padrão
            length = self.DEFAULT_LENGTH
            print(f"tamanho inválido. minimo de caractéres esperados é: ({self.DEFAULT_LENGTH})")

        # Gera senha aleatória
        return ''.join(random.choice(self.CHAR_POOL) for _ in range(length))


# Classe base Pessoa
class Pessoa:
    def __init__(self, nome: str):
        self.nome = nome


# Usuario herda de Pessoa e adiciona email
class Usuario(Pessoa):
    def __init__(self, nome: str, email: str):
        super().__init__(nome)
        self.email = email


# Categoria usando dataclass (mais simples)
@dataclass
class Categoria:
    nome: str


# Credencial representa um login (site + senha)
class Credencial(Usuario):
    def __init__(self, nome: str, email: str, site: str, senha, categoria: Categoria):
        super().__init__(nome, email)
        self.site = site
        self.senha = senha
        self.categoria = categoria
        
    # Mostra os dados da credencial
    def mostrar(self):
        return f"{self.nome} | {self.email} | {self.site} | {self.senha} | {self.categoria.nome}"


# Classe responsável por "criptografia" (simples reverso de string)
class Seguranca():
    def criptografar(self, senha):
        return senha[::-1]  # Inverte a string

    def descriptografar(self, senha):
        return senha[::-1]  # Reverte novamente


# Classe que armazena senha criptografada
class Encrypted(Credencial, Seguranca):
    def __init__(self, nome: str, email: str, site: str, senha, categoria: Categoria):
        super().__init__(nome, email, site, senha, categoria)
        # Ao criar, já salva a senha criptografada
        self.senha = self.criptografar(senha)

    # Ao mostrar, descriptografa a senha
    def mostrar(self):
        return f"{self.nome} | {self.email} | {self.site} | {self.descriptografar(self.senha)} | {self.categoria.nome}"


# Lista que funciona como "banco de dados"
cofre = []


# Classes de exceção personalizadas
class ErroDeCofre(Exception):
    pass


class SenhaErro(ErroDeCofre):
    pass


class NadaEncontrado(ErroDeCofre):
    pass


# Função para adicionar nova credencial
def Adicionar():
    try:
        nome = input("Digite seu nome:")
        site = input("Digite o nome do site/app:")
        email = input("Digite o email do site/app:")

        # Pergunta se quer gerar senha automática
        categ_op = input("Deseja gerar uma senha automatica? -> (S/N) ").strip()
        if categ_op.lower() == 's':
            gen = PswrdGenService()
            aux1 = input("digite o tamanho da senha ").strip()
            senha_length = int(aux1) if aux1.isdigit() else None
            senha = gen.gen_Pswrd(senha_length)
            print(f"senha gerada: {senha}")
        else:
            senha = input("Digite a senha do site/app:")

        categ = input("Digite a categoria do site/app:")

        # Validação simples
        if len(senha) < 4:
            raise SenhaErro("Senha muito curta!")

        categoria = Categoria(categ)
        c = Encrypted(nome, email, site, senha, categoria)

        cofre.append(c)  # Salva no "banco"

        print("Senha salva com sucesso")
        input("Pressione Enter para continuar...")

    except ErroDeCofre as e:
        print(f"ERRO! {e}")
        
    else:
        print("operacao finalizada!")
        
    finally:
        print("fim da operacao")


# Lista todas as credenciais
def Listar():
    try:
        if not cofre:
            raise NadaEncontrado("Cofre Vazio! Tente Novamente")

        for c in cofre:
            print(c.mostrar())

        input("Pressione Enter para continuar...")

    except ErroDeCofre as e:
        print(f"ERRO! {e}")


# Busca credencial por site
def Buscar():
    try:
        site = input("Digite o nome do site/app para buscar:")

        # FILTRO (OBS: aqui tem um pequeno bug de lógica)
        resultado = [c for c in cofre if c.site == site.lower()]

        if not resultado:
            raise NadaEncontrado("Nada encontrado")

        for c in resultado:
            print(c.mostrar())

        input("Pressione Enter para continuar...")

    except ErroDeCofre as e:
        print(f"ERRO! {e}")


# Deleta credencial
def Deletar():
    try:
        site = input("Digite o nome do site/app para deletar:")

        if not cofre:
            raise NadaEncontrado("Cofre vazio!")

        for c in cofre:
            if c.site.lower() == site.lower():
                cofre.remove(c)
                print("Deletado!")
                return

        raise NadaEncontrado("Site não encontrado")

    except ErroDeCofre as e:
        print(f"ERRO! {e}")


# Limpa o terminal (Windows/Linux)
def ClearTerminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# Menu principal
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

        # Estrutura de decisão (Python 3.10+)
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


# Inicia o programa
Menu()
