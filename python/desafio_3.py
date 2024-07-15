import textwrap
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional


def erro_operacao(motivo: str):
    return print(f"\n@@@ Falha na operação! ${motivo}. @@@")


class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas: List[Conta] = []

    def realizar_transacao(self, conta: 'Conta', transacao: 'Transacao'):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: 'Conta'):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero: int, cliente: Cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> 'Conta':
        return cls(numero, cliente)

    @property
    def saldo(self) -> float:
        return self._saldo

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def agencia(self) -> str:
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor: float) -> bool:
        if valor <= 0:
            erro_operacao("O valor informado é inválido.")
            return False
        if valor > self.saldo:
            erro_operacao("Você não tem saldo suficiente.")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True

    def depositar(self, valor: float) -> bool:
        if valor <= 0:
            erro_operacao("O valor informado é inválido.")
            return False

        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente: Cliente, limite: float = 500, limite_saques: int = 3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        if valor > self._limite:
            erro_operacao("O valor do saque excede o limite.")
            return False
        if numero_saques >= self._limite_saques:
            erro_operacao("Número máximo de saques excedido.")
            return False
        return super().sacar(valor)

    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes: List[dict] = []

    @property
    def transacoes(self) -> List[dict]:
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })


class Transacao(ABC):
    def __init__(self, valor: float):
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor

    @abstractmethod
    def registrar(self, conta: Conta):
        pass


class Saque(Transacao):
    def registrar(self, conta: Conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def registrar(self, conta: Conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_text))


def filtrar_cliente(cpf: str, clientes: List[Cliente]) -> Optional[Cliente]:
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def recuperar_conta_cliente(cliente: Cliente) -> Optional[Conta]:
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None
    return cliente.contas[0]


def depositar(clientes: List[Cliente]):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)


def sacar(clientes: List[Cliente]):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes: List[Cliente]):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        print("\n================ EXTRATO ================")
        transacoes = conta.historico.transacoes
        if not transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in transacoes:
                print(f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}")

        print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
        print("==========================================")


def criar_cliente(clientes: List[Cliente]):
    cpf = input("Informe o CPF (somente número): ")
    if filtrar_cliente(cpf, clientes):
        print("\n@@@ Já existe um cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta: int, clientes: List[Cliente], contas: List[Conta]):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas: List[Conta]):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes: List[Cliente] = []
    contas: List[Conta] = []

    while True:
        opcao = menu()
        match opcao:
            case "d":
                depositar(clientes)
            case "s":
                sacar(clientes)
            case "e":
                exibir_extrato(clientes)
            case "nu":
                criar_cliente(clientes)
            case "nc":
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)
            case "lc":
                listar_contas(contas)
            case "q":
                break
            case _:
                print(
                    "\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")


if __name__ == "__main__":
    main()
