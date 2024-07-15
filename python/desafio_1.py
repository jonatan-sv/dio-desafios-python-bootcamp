saldo         = 0
limite        = 500
extrato       = ""
numero_saques = 0
LIMITE_SAQUES = 3
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """


while True:
    opcao = input(menu)
    match opcao:
        case "d":
            valor = float(input("Informe o valor do depósito: "))

            if valor < 0:
                print("Falha na operação! O valor informado é inválido.")
            
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
                

        case "s":
            valor = float(input("Informe o valor do saque: "))
            # Erros
            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite
            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                print("Falha na operação! Você não tem saldo suficiente.")

            elif excedeu_limite:
                print("Falha na operação! O valor do saque excede o limite.")

            elif excedeu_saques:
                print("Falha na operação! Número máximo de saques excedido.")

            elif valor < 0:
                print("Falha na operação! O valor informado é inválido.")
            
            # Sucesso
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        case "e":
            print("\n================ EXTRATO ================")
            print("Não foram realizadas movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")

        case "q":
            break

        case _:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
