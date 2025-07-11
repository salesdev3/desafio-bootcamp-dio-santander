import textwrap

def menu():
    menu_text = f"""\n
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova conta
    [5] Listar contas
    [6] Novo usuário
    [0] Sair
    => """
    return input(textwrap.dedent(menu_text))

def depositar(saldo, valor_deposito, extrato, /):
    if valor_deposito > 0:
        saldo += valor_deposito
        extrato += f'Depósito:\tR${valor_deposito:.2f}\n'
        print('\n=== Depósito realizado com sucesso! ===')
    else:
        print('\nOperação falhou! O valor informado é inválido!')
    return saldo, extrato

def sacar(*, saldo, saque, extrato, VALOR_LIMITE_SAQUE, numero_saques, LIMITE_SAQUES):
    excedeu_saldo = saque > saldo
    excedeu_limite = saque > VALOR_LIMITE_SAQUE
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print('\nOperação falhou! Saldo insuficiente.')

    elif excedeu_limite:
        print('\nOperação falhou! O valor do saque excede o limite.')

    elif excedeu_saques:
        print('\nOperação falhou! Número máximo de saques atingido.')

    elif saque > 0:
        saldo -= saque
        extrato += f'Saque:\t\tR${saque:.2f}\n'
        numero_saques += 1
        print('\n=== Saque realizado com sucesso! ===')

    else:
        print('\nOperação falhou! O valor informado é inválido.')

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print('\n================ EXTRATO ================')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'\nSaldo:\t\tR$ {saldo:.2f}')
    print('==========================================')

def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente números): ')
    if filtrar_usuario(cpf, usuarios):
        print('\nJá existe um usuário com esse CPF!')
        return

    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa): ')
    endereco = input('Informe o endereço (Rua, n°, bairro, cidade, estado): ')

    usuarios.append({
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    })

    print('=== Usuário criado com sucesso! ===')

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    return None

def criar_conta(agencia, numero_conta, usuarios, contas):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print('\nUsuário não encontrado. Criação de conta cancelada.')
        return

    for conta in contas:
        if conta['usuario']['cpf'] == cpf:
            print('\nEste CPF já possui uma conta!')
            return

    conta = {
        'agencia': agencia,
        'numero_conta': numero_conta,
        'usuario': usuario,
        'saldo': 0,
        'extrato': '',
        'saques': 0
    }
    print('\n=== Conta criada com sucesso! ===')
    return conta

def listar_contas(contas):
    if not contas:
        print('\n=== Nenhuma conta cadastrada ===')
        return

    for conta in contas:
        linha = f"""
        Agência:\t{conta['agencia']}
        C/C:\t\t{conta['numero_conta']}
        Titular:\t{conta['usuario']['nome']}
        """
        print('=' * 50)
        print(textwrap.dedent(linha))

def selecionar_conta_por_cpf(contas):
    cpf = input('Informe o CPF do titular da conta: ')
    for conta in contas:
        if conta['usuario']['cpf'] == cpf:
            return conta
    print('\nConta não encontrada para este CPF.')
    return None

def iniciar_programa():
    LIMITE_SAQUES = 3
    VALOR_LIMITE_SAQUE = 500
    AGENCIA = '0001'

    usuarios = []
    contas = []

    while True:
        try:
            opcao = int(menu())
        except ValueError:
            print('Opção inválida. Digite um número.')
            continue

        if opcao == 1:
            conta = selecionar_conta_por_cpf(contas)
            if conta:
                valor = float(input('Informe o valor do depósito: '))
                conta['saldo'], conta['extrato'] = depositar(conta['saldo'], valor, conta['extrato'])

        elif opcao == 2:
            conta = selecionar_conta_por_cpf(contas)
            if conta:
                valor = float(input('Informe o valor do saque: '))
                conta['saldo'], conta['extrato'], conta['saques'] = sacar(
                    saldo=conta['saldo'],
                    saque=valor,
                    extrato=conta['extrato'],
                    VALOR_LIMITE_SAQUE=VALOR_LIMITE_SAQUE,
                    numero_saques=conta['saques'],
                    LIMITE_SAQUES=LIMITE_SAQUES
                )

        elif opcao == 3:
            conta = selecionar_conta_por_cpf(contas)
            if conta:
                exibir_extrato(conta['saldo'], extrato=conta['extrato'])

        elif opcao == 4:
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios, contas)
            if conta:
                contas.append(conta)

        elif opcao == 5:
            listar_contas(contas)

        elif opcao == 6:
            criar_usuario(usuarios)

        elif opcao == 0:
            print('\n=== Encerrando o programa... ===')
            break

        else:
            print('Opção inválida. Tente novamente.')

iniciar_programa()
