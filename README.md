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
| 10 | Salvar partida |
| 11 | Carregar partida |
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

## Bônus: interface medieval

- Limpeza da tela ao entrar nos menus e pausa com ENTER depois das operações.
- Artes ASCII, cores ANSI, cabeçalho de recursos, indicadores anuais e barra de prestígio.
- Classificação destacada e telas de promoção e vitória.
- Confirmação antes de sair ou substituir uma partida em andamento.
- Salvamento local em `partida.json` (opção 10) e carregamento (opção 11).
  O arquivo guarda os recursos, títulos, configurações, indicadores anuais, ano e vez atual.
  Um novo salvamento substitui o anterior. A partida atual não é alterada se o carregamento falhar.
- As oito etapas e os 37 testes originais foram preservados. Os 9 testes extras rodam com:

        python -m src.bolonhaemilano.testes_bonus

Use o terminal integrado do VS Code ou Windows Terminal. As pausas e a limpeza são
ativadas somente em terminal interativo. Para desativar as cores, defina a variável
`NO_COLOR` antes de executar o jogo. Nenhuma biblioteca externa é necessária.
Os diagramas do bônus têm o sufixo `-bonus`; os das etapas anteriores permanecem.
