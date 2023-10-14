# IMPORTAÇÕES
import os # Importar comandos do sistema operacional
from time import sleep # Importar comando do modulo time

# MENU PRINCIPAL:
menu = """
SEJA BEM VINDO AO BANCO PY

[ 1 ] - SAQUE
[ 2 ] - DEPOSITO
[ 3 ] - EXTRATO
[ 4 ] - SAIR

DIGITO ==>  """

# VARIAVEIS:

saldo = 0 
limite = 500
extrato = ""
numero_saques = 0 
LIMITE_SAQUES = 3

# ESTRUTURA DE REPETIÇÃO E DESENVOLVIMENTO DO CODIGO:
while True:

    opcao = int(input(menu)) # Opção para direcionar a alguma operação

    if opcao == 1:
        os.system('cls')
        try:
            valor = float(input('Digite a quantia que deseja depositar em sua conta bancária\n==> '))

            if numero_saques <= LIMITE_SAQUES: # Verifica o numero de saques feitos se é maior que o limite de saques;
                if valor > 0: # Verifica o valor que deseja sacar se é positivo;
                    if valor <= limite: # Verifica o valor que deseja sacar se é menor que o limite que pode sacar;
                        if valor <= saldo: # Verifica o valor que deseja sacar se é menor ou igual que o saldo;

                            os.system('cls')
                            novo_saldo = saldo - valor
                            print(f'Saque feito com sucesso!\n\nSALDO ANTERIOR: R${saldo:.2f}\nSALDO ATUAL: R${novo_saldo:.2f}')
                            saldo = saldo - valor
                            numero_saques += 1
                            extrato += f'SAQUE: R$ {valor:.2f}\n\n'
                            sleep(2)
                            os.system('cls')
                        else:
                            print('Você não possui esse valor na conta bancaria.')
                            sleep(2)
                            os.system('cls')
                    else:
                        print(f'Você so pode sacar R$ {limite},00 por saque')
                        sleep(2)
                        os.system('cls')                    
                else:
                    print('Digite somente valores positivos.')
                    sleep(2)
                    os.system('cls')    
            else:
                print(f'Você só pode realizar {LIMITE_SAQUES} por dia.')
                sleep(2)
                os.system('cls')
        except ValueError:
            print('Digite somente numeros.')
            sleep(2)
            os.system('cls')

    elif opcao == 2:
        os.system('cls')
        try:
            valor = float(input('Digite a quantia que deseja depositar em sua conta bancária\n==> '))

            if valor > 0: # Verifica o valor que deseja sacar se é positivo;
                os.system('cls')
                novo_saldo = saldo + valor
                print(f'Deposito feito com sucesso!\n\nSALDO ANTERIOR: R${saldo:.2f}\nSALDO ATUAL: R${novo_saldo:.2f}')
                saldo = saldo + valor
                extrato += f'DEPOSITO: R$ {valor:.2f}\n\n'
                sleep(3)
                os.system('cls')

            else:
                print('Digite somente valores positivos.')
                sleep(2)
                os.system('cls')
        except ValueError:
            print('Digite somente numeros.')
            sleep(2)
            os.system('cls')

    elif opcao == 3:
        print('Extrato Bancario:\n\n')
        print('Você não possui movimentações\n\n' if not extrato else extrato)
        print(f'R$ {saldo:.2f}')
        sleep(10)
        os.system('cls')

    elif opcao == 4:
        print('Saindo...')
        sleep(2)
        break

    else: 
        print('Operação invalida! por favor selecione novamente a operação desejada.')
        sleep(10)
        os.system('cls')
