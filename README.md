# Bolonha e Milano

Jogo de estratégia econômica medieval em Python, construído em 8 etapas incrementais.

## Como executar

Requisitos: Python 3.10+

    python -m src.bolonhaemilano.main

Não é necessário instalar bibliotecas externas nem compilar arquivos manualmente.

## Como jogar

Escolha de 1 a 4 jogadores. Cada jogador administra sua cidade até encerrar o turno.
O ano avança quando todos terminam a rodada. Colheita e impostos só podem ser
realizados uma vez por ano, por cidade.

| Opção | Ação |
| --- | --- |
| 1 | Novo jogo |
| 2 | Ver status da cidade |
| 3 | Mercado: comprar e vender grãos e terras |
| 4 | Agricultura: colher e distribuir alimentos |
| 5 | Governo: arrecadar impostos, definir taxa e justiça |
| 6 | Construções: recrutar soldados e construir |
| 7 | Encerrar turno |
| 8 | Ver classificação |
| 9 | Sobre o jogo |
| 0 | Sair (ou voltar, dentro de um submenu) |

O prestígio depende de construções, soldados, servos e terras. A cada fim de ano,
o governante pode subir um título. Vence quem chegar a Rei/Rainha ou quem tiver
o maior título ao fim de 1410 (desempate pelo prestígio).

## Como executar os testes

Na raiz do projeto:

    python -m src.bolonhaemilano.testes

Resultado esperado: `Aprovados: 37 | Reprovados: 0`.
Os testes cobrem as regras de Cidade, Mercado, Agricultura, Governo, Construcoes,
Jogador, Nobreza e Partida. Se uma verificação falhar, o processo termina com código 1.

## Estrutura

- `src/bolonhaemilano/` – código do jogo
- `casos-de-uso/` – diagramas de casos de uso
- `uml/` – diagramas de classes e de sequência

## Etapas

- [x] 1. Estrutura inicial, Main e menu
- [x] 2. Classes Jogador e Cidade
- [x] 3. Economia: florins, terras e grãos
- [x] 4. Agricultura e população
- [x] 5. Impostos e governo
- [x] 6. Construções e soldados
- [x] 7. Rodadas, múltiplos jogadores e vitória
- [x] 8. Integração, testes e entrega final
