# CONSTANTES
IDADE_MINIMA_DESCONTO = 65
PERCENTUAL_DESCONTO_IDADE = 0.20

VALOR_MINIMO_DESCONTO_EXTRA = 100.00
PERCENTUAL_DESCONTO_EXTRA = 0.10

QUANTIDADE_MINIMA_DESCONTO = 3
PERCENTUAL_DESCONTO_QUANTIDADE = 0.05

CUPOM_FIDELIDADE = "FIDELIDADE10"
PERCENTUAL_DESCONTO_CUPOM = 0.10

NOME_ARQUIVO_RESUMO = "resumo.txt"


# HISTÓRICO DO DIA
historico_compras = []


# CABEÇALHO
print("=" * 40)
print("        PDV - PONTO DE VENDA")
print("=" * 40)
print("Digite 0 no valor da compra para encerrar.\n")


# LOOP PRINCIPAL (uma volta = uma compra)
while True:

    # ENTRADA: valor da compra
    while True:
        texto_valor = input("Valor da compra (R$): ").strip().replace(",", ".")

        valor_eh_negativo = texto_valor.startswith("-")
        texto_valor_sem_sinal = texto_valor[1:] if valor_eh_negativo else texto_valor

        # Só dígitos, com no máximo um ponto decimal
        valor_eh_numero = texto_valor_sem_sinal.replace(".", "", 1).isdecimal()

        if not valor_eh_numero:
            print("⚠️  Valor inválido. Digite apenas números (ex: 150.50).")
        elif valor_eh_negativo:
            print("⚠️  O valor da compra não pode ser negativo.")
        else:
            valor_compra = float(texto_valor_sem_sinal)
            break

    # Valor 0 = sinal para encerrar o programa
    if valor_compra == 0:
        break

    # ENTRADA: idade do cliente
    while True:
        texto_idade = input("Idade do cliente: ").strip()

        idade_eh_negativa = texto_idade.startswith("-")
        texto_idade_sem_sinal = texto_idade[1:] if idade_eh_negativa else texto_idade

        idade_eh_numero = texto_idade_sem_sinal.isdecimal()

        if not idade_eh_numero:
            print("⚠️  Idade inválida. Digite um número inteiro (ex: 45).")
        elif idade_eh_negativa:
            print("⚠️  A idade não pode ser negativa.")
        else:
            idade_cliente = int(texto_idade_sem_sinal)
            break

    # ENTRADA: quantidade de itens
    while True:
        texto_quantidade = input("Quantidade de itens: ").strip()

        quantidade_eh_negativa = texto_quantidade.startswith("-")
        texto_quantidade_sem_sinal = (
            texto_quantidade[1:] if quantidade_eh_negativa else texto_quantidade
        )

        quantidade_eh_numero = texto_quantidade_sem_sinal.isdecimal()

        if not quantidade_eh_numero:
            print("⚠️  Quantidade inválida. Digite um número inteiro (ex: 3).")
        elif quantidade_eh_negativa:
            print("⚠️  A quantidade não pode ser negativa.")
        elif int(texto_quantidade_sem_sinal) == 0:
            print("⚠️  A compra precisa ter pelo menos 1 item.")
        else:
            quantidade_itens = int(texto_quantidade_sem_sinal)
            break

    # ENTRADA: cupom de fidelidade (opcional)
    texto_cupom = input("Cupom de fidelidade (Enter para pular): ").strip().upper()
    cupom = ""

    if texto_cupom == CUPOM_FIDELIDADE:
        cupom = texto_cupom
        print("✅ Cupom aplicado!")
    elif texto_cupom != "":
        print("⚠️  Cupom inválido. A compra seguirá sem cupom.")

    # DESCONTOS (cada um é aplicado sobre o valor que sobrou do anterior)
    valor_atual = valor_compra

    # Regra 1: desconto por idade
    percentual_idade = 0.0
    desconto_idade = 0.0
    if idade_cliente >= IDADE_MINIMA_DESCONTO:
        percentual_idade = PERCENTUAL_DESCONTO_IDADE
        desconto_idade = round(valor_atual * percentual_idade, 2)
        valor_atual = round(valor_atual - desconto_idade, 2)

    # Regra 2: desconto por valor (sobre o valor já descontado pela idade)
    percentual_valor = 0.0
    desconto_valor = 0.0
    if valor_atual > VALOR_MINIMO_DESCONTO_EXTRA:
        percentual_valor = PERCENTUAL_DESCONTO_EXTRA
        desconto_valor = round(valor_atual * percentual_valor, 2)
        valor_atual = round(valor_atual - desconto_valor, 2)

    # Bônus 1: desconto por quantidade
    percentual_quantidade = 0.0
    desconto_quantidade = 0.0
    if quantidade_itens > QUANTIDADE_MINIMA_DESCONTO:
        percentual_quantidade = PERCENTUAL_DESCONTO_QUANTIDADE
        desconto_quantidade = round(valor_atual * percentual_quantidade, 2)
        valor_atual = round(valor_atual - desconto_quantidade, 2)

    # Bônus 2: cupom de fidelidade
    percentual_cupom = 0.0
    desconto_cupom = 0.0
    if cupom == CUPOM_FIDELIDADE:
        percentual_cupom = PERCENTUAL_DESCONTO_CUPOM
        desconto_cupom = round(valor_atual * percentual_cupom, 2)
        valor_atual = round(valor_atual - desconto_cupom, 2)

    valor_final = valor_atual
    desconto_total = round(valor_compra - valor_final, 2)

    # RESULTADO DA COMPRA
    descontos = [
        ("idade", percentual_idade, desconto_idade),
        ("valor", percentual_valor, desconto_valor),
        ("quantidade", percentual_quantidade, desconto_quantidade),
        ("cupom", percentual_cupom, desconto_cupom),
    ]

    print("-" * 40)
    for nome, percentual, desconto in descontos:
        if percentual > 0:
            print(f"Desconto por {nome} ({percentual:.0%}): - R$ {desconto:.2f}")
    print(f"Valor final: R$ {valor_final:.2f}")
    print("-" * 40 + "\n")

    # GUARDA A COMPRA NO HISTÓRICO
    compra = {
        "valor_original": valor_compra,
        "idade": idade_cliente,
        "quantidade": quantidade_itens,
        "percentual_idade": percentual_idade,
        "percentual_valor": percentual_valor,
        "percentual_quantidade": percentual_quantidade,
        "percentual_cupom": percentual_cupom,
        "desconto_total": desconto_total,
        "valor_final": valor_final,
    }
    historico_compras.append(compra)


# RESUMO DO DIA
quantidade_compras = len(historico_compras)
total_bruto = 0.0
total_descontos = 0.0
total_final = 0.0

for compra in historico_compras:
    total_bruto += compra["valor_original"]
    total_descontos += compra["desconto_total"]
    total_final += compra["valor_final"]

print()

if quantidade_compras == 0:
    print("=" * 40)
    print("          RESUMO DO DIA")
    print("=" * 40)
    print("Nenhuma compra registrada.")
    print("=" * 40)

else:
    # TABELA DE COMPRAS
    cabecalho_tabela = (
        f"{'#':>3} | {'Valor (R$)':>12} | {'Idade':>5} | {'Qtd':>3} | "
        f"{'Desc. idade':>11} | {'Desc. valor':>11} | {'Desc. qtd':>9} | "
        f"{'Desc. cupom':>11} | {'Valor final':>13}"
    )

    print("COMPRAS DO DIA")
    print(cabecalho_tabela)
    print("-" * len(cabecalho_tabela))

    for numero, compra in enumerate(historico_compras, start=1):
        valor_final_texto = f"R$ {compra['valor_final']:.2f}"
        print(
            f"{numero:>3} | {compra['valor_original']:>12.2f} | "
            f"{compra['idade']:>5} | {compra['quantidade']:>3} | "
            f"{compra['percentual_idade']:>11.0%} | "
            f"{compra['percentual_valor']:>11.0%} | "
            f"{compra['percentual_quantidade']:>9.0%} | "
            f"{compra['percentual_cupom']:>11.0%} | "
            f"{valor_final_texto:>13}"
        )

    print("-" * len(cabecalho_tabela) + "\n")

    # RESUMO NO CONSOLE
    print("=" * 40)
    print("          RESUMO DO DIA")
    print("=" * 40)
    print(f"Compras registradas:  {quantidade_compras}")
    print(f"Total bruto:          R$ {total_bruto:.2f}")
    print(f"Total de descontos:   R$ {total_descontos:.2f}")
    print(f"Total final:          R$ {total_final:.2f}")
    print("=" * 40)

    # SALVAR RESUMO EM ARQUIVO
    # Só grava se houve compras, para não apagar um resumo anterior com um arquivo vazio
    with open(NOME_ARQUIVO_RESUMO, "w", encoding="utf-8") as arquivo:
        arquivo.write("RESUMO DO DIA\n")
        arquivo.write("=" * 40 + "\n\n")

        arquivo.write("Compras:\n")
        for numero, compra in enumerate(historico_compras, start=1):
            arquivo.write(
                f"{numero:>3}. valor R$ {compra['valor_original']:.2f} | "
                f"idade {compra['idade']} | "
                f"itens {compra['quantidade']} | "
                f"desconto R$ {compra['desconto_total']:.2f} | "
                f"final R$ {compra['valor_final']:.2f}\n"
            )

        arquivo.write("\n" + "=" * 40 + "\n")
        arquivo.write(f"Compras registradas:  {quantidade_compras}\n")
        arquivo.write(f"Total bruto:          R$ {total_bruto:.2f}\n")
        arquivo.write(f"Total de descontos:   R$ {total_descontos:.2f}\n")
        arquivo.write(f"Total final:          R$ {total_final:.2f}\n")

    print(f"\n💾 Resumo salvo em '{NOME_ARQUIVO_RESUMO}'.")