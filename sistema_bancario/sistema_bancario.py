menu = f"""
[{1}] Depositar
[{2}] Sacar
[{3}] Extrato
[{0}] Sair
=>"""

saldo = 0
VALOR_LIMITE_SAQUE = 500
numero_saques = 0
LIMITE_SAQUES = 3
extrato = ""

while True:
    
    opcao = int(input(menu).strip())
    
    if opcao == 1:
        valor_deposito = float(input('Digite o valor a ser depositado: R$'))
        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f'Depósito: R${valor_deposito:.2f}\n'
        
        else:
            print('Operação falhou! O valor informado é inválido!')
    
    elif opcao == 2:
        saque = float(input('Digite o valor a ser sacado: R$'))

        excedeu_limite = numero_saques >= LIMITE_SAQUES

        excedeu_saldo = saque > saldo

        excedeu_valor_limite = saque > VALOR_LIMITE_SAQUE

        if excedeu_limite:
            print('Operação falhou! O limite de saque diários foi atingido!')
        
        elif excedeu_saldo:
            print('Operação falhou! O valor digitado é maior que seu saldo!')

        elif excedeu_valor_limite:
            print('Operação falhou! O valor digitado é maior que o limite!')
        
        elif saque > 0:
            saldo -= saque
            extrato += f'Saque: R${saque:.2f}\n'
            numero_saques += 1

        else:
            print('Operação falhou! O valor informado é inválido!')

    elif opcao == 3:
        print('\n================ EXTRATO ================')
        print('Não foram realizadas movimentações!' if not extrato else extrato)
        print(f'\nSaldo: R${saldo:.2f}')
        print('==========================================')

    elif opcao == 0:
        break

    else:
        print('Operação inválida! Selecione novamente a opção desejada')