# Sistema Bancário


# função criar usuario
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Usuário criado com sucesso!")        
    
# Função filtrar usuario
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None    

# funcao criar conta
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        print(f"Agência: {agencia}")
        print(f"Número da conta: {numero_conta}")
        print(f"Titular: {usuario['nome']}")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("Usuário não encontrado, fluxo de criação de conta encerrado!")    
    return None

# funcao menu principal
def menu():
    menu = """\n
        ============================
            BANCO CEV - MENU
        ============================
        [1]\tCriar usuário
        [2]\tCriar conta corrente
        [3]\tDepositar
        [4]\tSacar
        [5]\tExtrato
        [6]\tListar usuários
        [7]\tListar contas
        [8]\tListar contas por usuário
        [9]\tSair
        => """ 
    return input(f"{menu} Escolha uma opção: ")

# Funções
# depósitos = []
def deposito(saldo, valor, extrato):
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return False

    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    return saldo, extrato

# saques = []
def saque(*,saldo, valor, extrato, limite, numero_saques, limite_saques):
    
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
    return saldo, extrato


# extrato = []
def imprimir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================") 

#funcao para listar usuarios
def listar_usuarios(usuarios):
    if usuarios == []:
        print("Nenhum usuário cadastrado.")
        return
    
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']}, CPF: {usuario['cpf']}, Data de Nascimento: {usuario['data_nascimento']}, Endereço: {usuario['endereco']}") 
        print("--------------------------------------------------")
        print()
        
#funcao para listar contas
def listar_contas(contas):
    if contas == []:
        print("Nenhuma conta cadastrada.")
        return
        
    for conta in contas:
        print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Titular: {conta['usuario']['nome']}")        
        print("--------------------------------------------------")
        print()
  
#funcao para listar contas por usuario
def listar_contas_usuario(usuarios, contas):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        contas_usuario = [conta for conta in contas if conta["usuario"]["cpf"] == cpf]
        
        if contas_usuario:
            for conta in contas_usuario:
                print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Titular: {conta['usuario']['nome']}")
                print("--------------------------------------------------")
                print()
        else:
            print("O usuário não possui contas.")
    else:
        print("Usuário não encontrado.")    


#funcao principal
def main():
    
    saldo = 0
    limite = 500
    extrato = ""
    usuarios = []
    contas = []


    # Variáveis de controle
    numero_saques = 0
    numero_conta = 1
    
    #constantes
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    ## Loop principal
    while True:

        opcao = menu()
        if opcao == "1":
            criar_usuario(usuarios)
            
        elif opcao == "2":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta) 
                numero_conta += 1
            
        elif opcao == "3":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = deposito(saldo, valor, extrato)
            
        elif opcao == "4":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = saque(saldo=saldo,valor=valor, extrato=extrato, limite=limite,numero_saques=numero_saques,limite_saques=LIMITE_SAQUES)
            
        elif opcao == "5":
            imprimir_extrato(saldo, extrato=extrato)
        
        elif opcao == "6":
            listar_usuarios(usuarios)
            
        elif opcao == "7":
            listar_contas(contas)   

        elif opcao == "8":
            listar_contas_usuario(usuarios, contas)

        elif opcao == "9":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()