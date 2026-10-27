# PDV - Ponto de Venda com Descontos Progressivos (Nível 1)

## O que o código faz

Este programa simula o caixa de uma loja. Para cada compra, ele recebe o valor,
a idade do cliente, a quantidade de itens e um cupom opcional, aplica descontos
progressivos de acordo com regras de negócio e mostra o valor final em reais.
Várias compras podem ser registradas em sequência. Quando o usuário digita `0`
no valor da compra, o programa encerra, exibe uma tabela com todas as compras
do dia, mostra o resumo (quantidade de compras, total bruto, total de descontos
e total final) e grava esse resumo no arquivo `resumo.txt`.

## Como ele faz

1. Pede o **valor da compra** e confere se é um número válido e não negativo.
   Se não for, mostra um aviso e pede novamente. Aceita vírgula ou ponto
   (`10,50` ou `10.50`).
2. Se o valor for `0`, o loop termina e o programa vai para o resumo final.
3. Pede a **idade do cliente**, a **quantidade de itens** e o **cupom**.
   Idade e quantidade são validadas (inteiros, sem negativos; a quantidade
   também não pode ser zero). O cupom pode ficar em branco.
4. Aplica os descontos nesta ordem, cada um sobre o valor que sobrou do anterior:
   1. **Idade:** se a idade for maior ou igual a 65, desconto de 20%.
   2. **Valor:** se o valor já descontado pela idade for maior que R$ 100,00,
      desconto extra de 10%.
   3. **Quantidade (bônus):** se houver mais de 3 itens, desconto extra de 5%.
   4. **Cupom (bônus):** se o cupom for `FIDELIDADE10`, desconto extra de 10%.
5. Arredonda cada etapa para 2 casas decimais e exibe o valor final
   (ex.: `R$ 144.00`).
6. Guarda a compra numa lista (`historico_compras`) com `.append()` e volta ao
   passo 1.
7. Ao encerrar, percorre a lista com um `for`, soma os valores e mostra a
   tabela de compras e o resumo do dia.
8. Grava o resumo no arquivo `resumo.txt` usando `open(..., "w")` e um `for`
   na lista. Se nenhuma compra foi feita, o arquivo não é gravado, para não
   apagar um resumo anterior.

As regras ficam em constantes no topo do `pdv.py` (`IDADE_MINIMA_DESCONTO`,
`PERCENTUAL_DESCONTO_IDADE` etc.), então para mudar uma regra basta alterar
o valor ali.

## Como rodar

```bash
python pdv.py
```

Para cada compra, o programa pergunta, nesta ordem: valor, idade, quantidade
de itens e cupom (Enter para pular). Digite `0` no valor da compra para encerrar.

## Tabela de exemplos (casos de teste)

Nestes casos, use **1** na quantidade de itens e aperte **Enter** no cupom
(sem bônus), para conferir só as regras de idade e valor.

| #  | Valor (R$) | Idade | Desconto idade | Desconto valor | Valor final esperado |
|----|------------|-------|----------------|----------------|----------------------|
| 1  | 50.00      | 30    | 0%             | 0%             | R$ 50.00             |
| 2  | 100.00     | 30    | 0%             | 0%             | R$ 100.00            |
| 3  | 80.00      | 65    | 20%            | 0%             | R$ 64.00             |
| 4  | 100.00     | 70    | 20%            | 0%             | R$ 80.00             |
| 5  | 125.00     | 70    | 20%            | 0%             | R$ 100.00            |
| 6  | 200.00     | 30    | 0%             | 10%            | R$ 180.00            |
| 7  | 101.00     | 30    | 0%             | 10%            | R$ 90.90             |
| 8  | 200.00     | 65    | 20%            | 10%            | R$ 144.00            |
| 9  | 1000.00    | 80    | 20%            | 10%            | R$ 720.00            |
| 10 | 200.00     | 64    | 0%             | 10%            | R$ 180.00            |

Casos-limite:

- **Caso 2:** 100,00 não é *maior* que 100, então não recebe o desconto de valor.
- **Caso 5:** 125 x 0,8 = 100,00. Como não é maior que 100, os 10% não se aplicam.
- **Caso 7:** 101 x 0,9 = 90,90 (arredondado para 2 casas decimais).
- **Caso 10:** a idade é 64, então não há desconto por idade, só o de valor.

Rodando esses 10 casos em sequência, o resumo final deve mostrar:

- Compras registradas: 10
- Total bruto: R$ 2156.00
- Total de descontos: R$ 447.10
- Total final: R$ 1708.90

## Exemplos dos bônus

| Valor (R$) | Idade | Itens | Cupom          | Cálculo                                      | Valor final esperado |
|------------|-------|-------|----------------|----------------------------------------------|----------------------|
| 200.00     | 30    | 4     | (nenhum)       | 200 x 0,9 = 180; 180 x 0,95                  | R$ 171.00            |
| 200.00     | 30    | 1     | FIDELIDADE10   | 200 x 0,9 = 180; 180 x 0,9                   | R$ 162.00            |
| 200.00     | 65    | 5     | FIDELIDADE10   | 160; 144; 136,80; 136,80 x 0,9               | R$ 123.12            |
| 50.00      | 30    | 4     | (nenhum)       | só o desconto de quantidade: 50 x 0,95       | R$ 47.50             |
| 100.00     | 30    | 3     | (nenhum)       | 3 itens não é *mais* que 3: sem desconto     | R$ 100.00            |

## Arquivo gerado

Ao final, o programa cria o arquivo `resumo.txt` na pasta em que o comando foi
executado, com uma linha por compra e os totais do dia.