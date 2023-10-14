# IMPORTAÇÕES
import os # Importar comandos do sistema operacional
from time import sleep, gmtime, strftime # Importar comando do modulo time

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

def limpar():
    sleep(3)
    os.system('cls')

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):

    valor_negativo = valor < 0 
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques > limite_saques

    if valor_negativo: 
        print('O valor do saque não pode ser negativo.')
        limpar()
    elif excedeu_saldo: 
        print('O valor do saque não pode ser maior que o saldo.')
        limpar()

    elif excedeu_limite: 
        print(f'O valor do saque não pode ser maior que o limite por operação.\nO seu limite é R${limite:.2f}')
        limpar()

    elif excedeu_saques: 
        print(f'Você ja ultrapassou o limite de saque diario\nO seu limite são {limite} saque(s) diario.')
        limpar()

    elif not valor_negativo:
        novo_saldo = saldo - valor
        print(F'Saque realizado com sucesso!\n\nSALDO ANTERIOR: {saldo:.2f}\nSALDO ATUAL: {novo_saldo:.2f}')
        saldo -= valor
        numero_saques += 1
        extrato += f'SAQUE ({strftime("%d %b %Y", gmtime())}):VALOR: {valor:.2f}\t SALDO: {saldo:.2f}\n'
        limpar()

    return saldo, extrato


def depositar(saldo, valor, extrato, /):

    try:
        if valor > 0:
            novo_saldo = saldo + valor
            print(F'Deposito realizado com sucesso!\n\nSALDO ANTERIOR: {saldo:.2f}\nSALDO ATUAL: {novo_saldo:.2f}')
            saldo += valor
        
            extrato += f'DEPOSITO ({strftime("%d %b %Y", gmtime())}):VALOR: {valor:.2f}\t SALDO: {saldo:.2f}\n'
            limpar()
    except ValueError: 
        print('Possiveis erros:\n- O valor não pode está em branco.\n- O valor deve ser um numero.\n- O valor não deve conter virgulas, substitua por ponto.')
        limpar()
    return saldo, extrato


def exibir_extrato(extrato,*, saldo):
    print('============== EXTRATO ==============\n')
    print('Você não possui movimentação.\n' if not extrato else extrato)
    print(f'\nSaldo: R${saldo:.2f}')
    print('=====================================')
    sleep(10)
    return extrato, saldo            

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado, fluxo de criação de conta encerrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(linha)

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuario(usuarios):
    cpf = input("DIGITE SEU CPF (SOMENTE NUMEROS): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF!")
        return
    
    nome = input("DIGITE SEU NOME: ")
    cpf = input("DIGITE SEU CPF (SOMENTE NUMEROS): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado):")

    usuarios.append({'nome': nome, 'cpf': cpf, 'endereço': endereco})
    print('Usuario criado com sucesso!')
    limpar() 

def main():

    # VARIAVEIS:
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 1000 
    limite = 500
    extrato = ""
    numero_saques = 0 
    usuarios = []
    contas = []

    while True:

        opcao = int(input(menu()))

        if opcao == 1:
            os.system('cls')
            try:
                valor = float(input('DIGITE O VALOR DO SAQUE:'))
                
                saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

            except ValueError: 
                print('Possiveis erros:\n- O valor não pode está em branco.\n- O valor deve ser um numero.\n- O valor não deve conter virgulas, substitua por ponto.')
                limpar()
       
        elif opcao == 2:
            os.system('cls')
            try:
                valor = float(input('DIGITE O VALOR DO DEPOSITO:'))
                
                saldo, extrato = depositar(saldo,valor,extrato,)
                
            except ValueError: 
                print('Possiveis erros:\n- O valor não pode está em branco.\n- O valor deve ser um numero.\n- O valor não deve conter virgulas, substitua por ponto.')
                limpar()

        elif opcao == 3:
            exibir_extrato(extrato, saldo=saldo)
            limpar()
                        
        elif opcao == 4:
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == 5:
            listar_contas(contas)

        elif opcao == 6:
            criar_usuario(usuarios)
            
        elif opcao == 0:
            break


main()