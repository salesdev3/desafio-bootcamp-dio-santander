import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\nAgência:\t{conta.agencia}
Número:\t{conta.numero}
Titular:\t{conta.cliente.nome}
Saldo:\t\tR$ {conta.saldo:.2f}"""
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    """Classe base para clientes."""

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
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    """Classe base para contas bancárias."""

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
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
        if valor <= 0:
            print('Operação falhou! O valor é inválido!')
            return False

        if valor > self.saldo:
            print('\nOperação falhou! Você não tem saldo suficiente!')
            return False

        self._saldo -= valor
        print('Saque efetuado!')
        return True

    def depositar(self, valor):
        if valor <= 0:
            print('\nOperação falhou! O valor informado é inválido!')
            return False

        self._saldo += valor
        print('\nDepósito efetuado!')
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([
            t for t in self.historico.transacoes if t['tipo'] == Saque.__name__
        ])
        if valor > self._limite:
            print('\nOperação falhou! O valor de saque excede o limite!')
        elif numero_saques >= self._limite_saques:
            print('\nOperação falhou! Número máximo de saques excedido!')
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\nAgência:\t{self.agencia}
C/C:\t\t{self.numero}
Titular:\t{self.cliente.nome}
"""


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime('%H:%M:%S'),
            }
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if (
                tipo_transacao is None or
                transacao['tipo'].lower() == tipo_transacao.lower()
            ):
                yield transacao


class Transacao(ABC):
    @property
    @abstractmethod
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
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        print(f'{datetime.now()}: {func.__name__.upper()}')
        return resultado
    return envelope


def exibir_menu():
    menu_texto = '''\n ================ MENU ================
[1] Depositar
[2] Sacar
[3] Extrato
[4] Nova Conta
[5] Listar Contas
[6] Novo usuário
[0] Sair
=> '''
    return input(textwrap.dedent(menu_texto))


def filtrar_cliente(cpf, clientes):
    return next((cliente for cliente in clientes if cliente.cpf == cpf), None)


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('\nCliente não possui conta!')
        return None
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('\nCliente não encontrado!')
        return

    try:
        valor = float(input('Informe o valor do depósito: '))
    except ValueError:
        print('\nValor inválido! Use apenas números.')
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        transacao = Deposito(valor)
        cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('\nCliente não encontrado!')
        return

    try:
        valor = float(input('Informe o valor do saque: '))
    except ValueError:
        print('\nValor inválido! Use apenas números.')
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        transacao = Saque(valor)
        cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print('\n================ EXTRATO ================')
    extrato = ''
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += (
            f"\n{transacao['tipo']}:\n\t"
            f"R$ {transacao['valor']:.2f} às {transacao['data']}"
        )

    if not tem_transacao:
        extrato = 'Não foram realizadas movimentações'
    print(extrato)
    print(f'\nSaldo:\n\tR$ {conta.saldo:.2f}')
    print('=========================================')


@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    if filtrar_cliente(cpf, clientes):
        print('\nJá existe um cliente com esse CPF!')
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, n° - bairro - cidade/estado): ")

    cliente = PessoaFisica(
        nome=nome,
        data_nascimento=data_nascimento,
        cpf=cpf,
        endereco=endereco
    )
    clientes.append(cliente)
    print('\n=== Cliente criado! ===')


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print('\nCliente não encontrado!')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print('\n=== Conta criada com sucesso! ===')


def listar_contas(contas):
    if not contas:
        print('\nNenhuma conta cadastrada.')
        return

    for conta_str in ContasIterador(contas):
        print('=' * 40)
        print(textwrap.dedent(conta_str))


def main():
    clientes = []
    contas = []

    while True:
        try:
            opcao = int(exibir_menu())
        except ValueError:
            print('\nEntrada inválida! Digite um número.')
            continue

        if opcao == 1:
            depositar(clientes)
        elif opcao == 2:
            sacar(clientes)
        elif opcao == 3:
            exibir_extrato(clientes)
        elif opcao == 4:
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == 5:
            listar_contas(contas)
        elif opcao == 6:
            criar_cliente(clientes)
        elif opcao == 0:
            print('\nEncerrando...')
            break
        else:
            print('\nOperação inválida, tente novamente!')


if __name__ == '__main__':
    main()