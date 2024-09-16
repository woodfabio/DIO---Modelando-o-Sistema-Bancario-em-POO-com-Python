# Imports:
from abc import ABC, abstractproperty, abstractclassmethod

# --------------------------------------------------------------------------------------------------------------
# Classes:
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        # filtrar conta
        conta_filtrada = None
        for c in self._contas:
            if int(c.getNumero) == int(conta):
                conta_filtrada = c

        if conta_filtrada is not None:
            transacao.registrar(conta_filtrada)
        else:
            print("Conta inexistente")

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def getEndereco(self):
        return self._endereco
    
    @property
    def getContas(self):
        return self._contas

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def getCpf(self):
        return self._cpf
    
    @property
    def getNome(self):
        return self._nome

    @property
    def getDataNascimento(self):
        return self._data_nascimento

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        check = conta.depositar(self.valor)

        if check:
            conta._historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        check = conta.sacar(self.valor)

        if check:
            conta._historico.adicionar_transacao(self)    

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({"tipo":transacao.__class__.__name__, "valor":transacao.valor})

class Conta:
    def __init__(self, saldo, numero, cliente):
        self._saldo = saldo
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def getSaldo(self):
        return self._saldo
    
    @property
    def getNumero(self):
        return self._numero
    
    @property
    def getAgencia(self):
        return self._agencia
    
    @property
    def getCliente(self):
        return self._cliente
    
    @property
    def getHistorico(self):
        return self._historico
    
    def sacar(self, valor):
        check = valor > self._saldo

        if check:
            print("Saldo insuficiente.")
        elif valor <= 0:
            print("Valor invalido.")
        else:
            self._saldo -= valor
            print(f"Saque efetuado no valor de R${valor:.2f}")
            return True

    def depositar(self, valor):

        if valor <= 0:
            print("Valor invalido.")
        else:
            self._saldo += valor
            print(f"Deposito efetuado no valor de R${valor:.2f}")
            return True

class ContaCorrente(Conta):
    def __init__(self, saldo, numero, cliente, limite = 500, limite_saques = 3):
        super().__init__(saldo, numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def getLimite(self):
        return self._limite
    
    @property
    def getLimite_saques(self):
        return self._limite_saques
    
    def sacar(self, valor):
        saques = 0
        for transacao in self._historico.transacoes:
            if transacao["tipo"] == Saque.__name__:
                saques += 1
        
        if saques >= self._limite_saques:
            print("Numero de saques diarios excedido.")
        elif valor > self._limite:
            print("Valor excedeu o limite de saque.")
        else:
            return super().sacar(valor)

    def __str__(self):
        return f"Agência: {self._agencia}\nC/C: {self._numero}\nTitular: {self._cliente.getNome()}"

# --------------------------------------------------------------------------------------------------------------
# Variables:

menu = """

=================
[d] Depositar
[s] Sacar
[u] Novo usuario
[c] Nova conta
[e] Extrato
[l] Listar contas
[q] Sair
=================

=>"""

usuarios = []
clientes = []
numero_conta = 1

# --------------------------------------------------------------------------------------------------------------
# Functions:

def check_numero(num):
    if num.isnumeric():
        return float(num)

def deposito(valor_deposito, cpf, clientes, conta): 
    
    # verificar se o usuario esta cadastrado
    cliente = None
    for c in clientes:
        if c.getCpf == cpf:
            cliente = c

    if cliente is None:
        print("Titular nao cadastrado.")
        return
    else:
        if valor_deposito is None:
            print("Insira um valor numérico positvo.")
        else:
            transacao = Deposito(valor_deposito)
            cliente.realizar_transacao(conta, transacao)
    
def saque(*, valor, cpf, clientes, conta):

    # verificar se o usuario esta cadastrado
    cliente = None
    for c in clientes:
        if c.getCpf == cpf:
            cliente = c

    if cliente is None:
        print("Titular nao cadastrado.")
        return
    else:
        if valor is None:
            print("Insira um valor numérico positvo.")
        else:
            transacao = Saque(valor)
            cliente.realizar_transacao(conta, transacao)
    
def criar_usuario(usuarios, cpf):

    if cpf is None:
        print("Insira um valor numérico positvo.")
    else:
        cliente_existe = False
        for c in clientes:
            if c.getCpf == cpf:
                cliente_existe = True

        if cliente_existe:
            print("Cliente ja cadastrado.")
        else:
            nome = input("Insira nome: ")
            data_nasc = input("Insira a data de nascimento (dd-mm-aaa): ")
            endereco = input("Insira endereco (logradouro, numero, bairro, cidade, sigla estado): ")

            novo_usuario = PessoaFisica(endereco, cpf, nome, data_nasc)
            clientes.append(novo_usuario)
            print("Usuario registrado")

def criar_conta(cpf, clientes, numero_conta):

    if cpf is None:
        print("Insira um valor numérico positvo.")
    else:
        # verificar se o usuario esta cadastrado
        cliente = None
        for c in clientes:
            if c.getCpf == cpf:
                cliente = c

        if cliente is None:
            print("Titular inexistente.")
        else:            
            nova_conta = ContaCorrente(0, numero_conta, cliente)
            cliente.adicionar_conta(nova_conta)
            print(f"Conta criada.")

def extrato(clientes):

    # filtrar cliente
    cpf = input("Informe o CPF: ")
    cliente = None
    for c in clientes:
        if c.getCpf == cpf:
            cliente = c

    if cliente is None:
        print("Cliente inexistente.")
    else:
        # filtrar conta
        conta_num = input("Informe numero da conta: ")
        conta_filtrada = None
        for conta in cliente._contas:
            if int(conta.getNumero) == int(conta_num):
                conta_filtrada = conta
        
        if conta_filtrada is None:
            print("Conta inexistente.")
        else:
            print("=========== EXTRATO ===========")
            extrato = ""
            transacoes = conta_filtrada.getHistorico.transacoes
            
            if len(transacoes) == 0:
                print("Nenhuma transacao efetuada.")
            else:
                for transacao in transacoes:
                    extrato += f"{transacao['tipo']}: R${transacao['valor']:.2f}\n"
                print(extrato)
                print(f"\nSaldo: R${conta_filtrada.getSaldo:.2f}")
            
            print("===============================")

def listar_contas(clientes):
    # filtrar cliente
    cpf = input("Informe o CPF: ")
    cliente = None
    for c in clientes:
        if c.getCpf == cpf:
            cliente = c

    if cliente is None:
        print("Cliente inexistente.")
    else:
        for conta in cliente.getContas:
            print("---------------------")
            print(f"{conta.getAgencia} - {conta.getNumero}")

# --------------------------------------------------------------------------------------------------------------
# Main program:

while True:

    opcao = input(menu)

    if opcao == "d": # deposito

        cpf = input("CPF do titular (apenas numeros): ")
        conta = input("Numero da conta do titular: ")
        valor_deposito = input("Valor do depósito R$: ")
        valor_deposito = check_numero(valor_deposito)

        deposito(valor_deposito, cpf, clientes, conta)

    elif opcao == "s": # saque

        cpf = input("CPF do titular (apenas numeros): ")
        conta = input("Numero da conta do titular: ")
        valor_saque = input("Valor do saque R$: ")
        valor_saque = check_numero(valor_saque)

        saldo = saque(valor=valor_saque, cpf=cpf, clientes=clientes, conta=conta)

    elif opcao == "u": # novo usuario

        cpf = input("Inserir CPF (somente numeros): ")
        criar_usuario(usuarios, cpf)

    elif opcao == "c": # nova conta

        cpf = input("Inserir CPF (somente numeros): ")

        criar_conta(cpf, clientes, numero_conta)
        numero_conta += 1

    elif opcao == "e":

        extrato(clientes)

    elif opcao == "l":

        listar_contas(clientes)

    elif opcao == "q": # sair

        break

    else:

        print("Operação inválida, por favor selecione novamente a operação desejada.")