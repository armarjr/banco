from abc import ABC,  abstractmethod
from datetime import datetime
import  textwrap


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento=data_nascimento 
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo=0
        self._agencia= "0001"
        self._numero= numero
        self._cliente = cliente
        self._historico = Historico()
        
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
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
         
        if excedeu_saldo:
            print ("Operacao falhou. Voce nao tem saldo suficiente")
        elif valor >0:
            self._saldo -= valor
            print ("Operacao realizada com sucesso.")
            return True
        else:
            print ("valor informado invalido.")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print ("Deposito realizado com sucesso.")
        else:
            print ("valor informado invalido.add()")
            return False
        
        return True
        
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self.limite
        
        excedeu_saques = numero_saques >= self.limite_saques
        
        if excedeu_limite:
            print("Operacao falhou. O valor excedeu limite de saque.")
        elif excedeu_saques:
            print("Operacao falhou. Excedeu a quantidade de saques permitido")
        else:
            return super().sacar(valor )       
        
        return False
    
    def __str__(self):
        return f"""\
            Agencia:\t {self.agencia} 
            c/c:\t\t {self.numero}
            Titular: \t{self.cliente.nome}   
            """

class Historico:
    def __init__(self):
        self._transacoes =[]
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {"tipo":transacao.__class__.__name__,
            "valor": transacao.valor, 
            "data": datetime.now().strftime("%d-%m-%Y H:%M")
            }
        )

class Transacao(ABC):
    @property
    def valor(self):
        pass
    
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
        
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
    
class Deposito(Transacao):
    def __init__(self , valor):
        self._valor = valor
    
    @property
    def  valor(self):
        return self._valor   
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Funções

# Função filtrar cliente
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None    


# funcao menu principal
def menu():
    menu = """\n
        ============================
            BANCO CEV - MENU
        ============================
        [1]\tCriar clientes
        [2]\tCriar conta corrente
        [3]\tDepositar
        [4]\tSacar
        [5]\tExtrato
        [6]\tListar clientes
        [7]\tListar contas
        [9]\tSair
        => """ 
    return input(f"{menu} Escolha uma opção: ")

# recuperar contas do cliente
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente nao possui conta.")
        return
    
    # fixo cliente nao pode escolher conta 
    
    return cliente.contas[0]

# depositar
def depositar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente nao encontrado.")
        return
        
    valor = float(input("Digite o valor do deposito: "))
    
    transacao = Deposito(valor)
    
    conta = recuperar_conta_cliente(cliente)
    
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# sacar
def sacar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente nao encontrado.")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente nao encontrado.")
        return
        
    valor = float(input("Digite o valor do saque: "))
    
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(cliente)
    
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# exibir extrato
def exibir_extrato(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente nao encontrado.")
        return
        
    conta = recuperar_conta_cliente(cliente)
    
    if not conta:
        return
    
    print("\n ***************** Extrato ****************")
    
    transacoes= conta.historico.transacoes
    extrato = ""
    
    if not transacoes:
        extrato = "Nao foram realizadas transacoes."
    else:
        for transacao in transacoes:
            extrato += f"\n {transacao['tipo']}:\n\t R$ {transacao['valor']:.2f}"
    
    print (extrato)
    print(f"\nSaldo: \n\t R${conta.saldo:.2f} ")
    print("******************************************")

# criar cliente 
def criar_cliente(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if cliente:
        print("Ja existe Cliente com este cpf.")
        return

    nome = input("Informe nome completo: ")
    
    data_nascimento= input("Informe data nascimento (dd-mm-aaaa): ")
    
    endereco = input("Informe o endereco(logradouro- bairro - cidade /sigla do Estado): ")
    
    cliente= PessoaFisica(nome=nome, data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)
    
    clientes.append(cliente)
    
    print ("Cliente criado com sucesso")


# criar conta 
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("Cliente nao encontrado.")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)

    contas.append(conta)
    cliente.contas.append(conta)
    print ("Conta criada com sucesso.")

#listar contas 
def listar_contas(contas):
    for conta in contas:
        print ("*" * 50)
        print (textwrap.dedent(str(conta)))
        
#listar clientes 
def listar_clientes(clientes):
    if not clientes:
        print("Nao existem clientes cadastrados")
        return
    
    for cliente in clientes:
        print("*" * 50)
        print(f"\nCpf: {cliente.cpf} \nNome: {cliente.nome} \nEndereco: {cliente.endereco} ")
        

#funcao principal
def main():
    clientes = []
    contas = []

    ## Loop principal
    while True:

        opcao = menu()
        if opcao == "1":
            criar_cliente(clientes)
            
        elif opcao == "2":
            numero_conta = len(contas)+1
            criar_conta(numero_conta, clientes, contas)
            
        elif opcao == "3":
            depositar(clientes)
            
        elif opcao == "4":
            sacar(clientes)
             
        elif opcao == "5":
            exibir_extrato(clientes)
            
        elif opcao == "6":
            listar_clientes(clientes)
            
        elif opcao == "7":
            listar_contas(contas)   

        elif opcao == "9":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()