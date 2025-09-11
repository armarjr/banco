# Sistema Bancário

## Variáveis e constantes

menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[9] Sair

=> """

saldo = 0
limite = 500
extrato = ""

# Variáveis de controle
numero_saques = 0
LIMITE_SAQUES = 3

# Funções
# depósitos = []
def deposito(*, valor):
    global saldo, extrato
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return False

    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    return True, saldo, extrato

# saques = []
def saque(*, valor, limite,limite_saques):
    global saldo, extrato, numero_saques
    
    if valor <= 0 or valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return False

    if valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return False

    if numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return False

    saldo -= valor
    numero_saques += 1
    extrato += f"Saque: R$ {valor:.2f}\n"
    print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
    return True, saldo, extrato, numero_saques

# extrato = []
def imprimir_extrato(saldo, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================") 

## Loop principal


while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: "))

        deposito(valor=valor)
        
    elif opcao == "2":
        valor = float(input("Informe o valor do saque: "))

        saque(valor=valor, limite=limite, limite_saques=LIMITE_SAQUES)        
        
    elif opcao == "3":
        imprimir_extrato(saldo, extrato)
    elif opcao == "9":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")