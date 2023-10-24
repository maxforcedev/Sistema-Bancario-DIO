from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime
import os

class Cliente:
    def __init__(self, endereco):
        self.endereco = str(endereco)
        self.contas = []    
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = str(cpf)
        self.nome = str(nome)
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = int(numero)
        self._agencia = '0001'
        self._cliente = cliente
        self._historico  = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._Historico
    
    def sacar(self,valor):
        saldo = self.saldo
        saldo_anterior = saldo

        if saldo > valor:
            print('Operação cancelada! Você não possui saldo suficiente.')
        else:
            print('Algo de errado ocorreu! Tente novamente.')

        if valor > 0:
            self._saldo -= valor
            print(f'Saque realizado com sucesso!\n\nSALDO ANTERIOR: R${saldo_anterior:.2F}\nSALDO ATUAL: R${self._saldo:.2F}')
            return True
        else:
            print('Operação cancelada! Você não pode sacar um valor negativo')
       
        return False
    
    def depositar(self,valor):
        saldo = self.saldo
        saldo_anterior = saldo

        if saldo > valor:
            print('Operação cancelada! Você não possui saldo suficiente.')
        else:
            print('Algo de errado ocorreu! Tente novamente.')
       
        if valor > 0:
            self._saldo += valor
            print(f'Deposito realizado com sucesso!\n\nSALDO ANTERIOR: R${saldo_anterior:.2F}\nSALDO ATUAL: R${self._saldo:.2F}')
            return True
        else:
            print('Operação cancelada! Você não pode depositar um valor negativo')
        
        return False    
    

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([ transacao for transacao in self.historico.transacoes if transacao['tipo'] == Saque.__name__])

        if valor > self.limite:
            print(f"Operação cancelada! Você ultrapassou o seu limite de R$ {self.limite} reais.")
        
        elif numero_saques > self.limite_saques:
            print(f"Operação cancelada! Você ultrapassou o seu limite de saques diarios.")

        else:
            return super().sacar(valor)
        
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
    """

        
class Historico:
    def __init__(self):
        self.transacoes = [ ]

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime("%d-%M-%Y %H:%M:%s")
        })


class Transacao(ABC):


    @property
    @abstractproperty
    def valor(self):
        pass
    @abstractproperty
    def registrar(self, conta):
        pass


class Saque(Transacao):

    def __init__(self) -> None:
        super().__init__()

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Depositar(Transacao):

    def __init__(self) -> None:
        super().__init__()

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """
SEJA BEM VINDO AO BANCO PY

[ 1 ] - SAQUE
[ 2 ] - DEPOSITO
[ 3 ] - EXTRATO
[ 4 ] - CRIAR CONTA
[ 5 ] - LISTAR CONSTAS
[ 6 ] - NOVO USUARIO
[ 0 ] - SAIR

DIGITO ==>  """
    return menu

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta! ")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado! ")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado! ")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado! ")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n= EXTRATO =")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF! ")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n Cliente criado com sucesso! ")
 

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado, fluxo de criação de conta encerrado! ")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n Conta criada com sucesso! ")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(conta)


def main():
    clientes = []
    contas = []

    while True:
        opcao = input(menu())

        if opcao == "1":
            sacar(clientes)

        elif opcao == "2":
            depositar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "5":
            listar_contas(contas)

        elif opcao == "6":
            criar_cliente(clientes)

        elif opcao == "0":
            break

        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")


main()