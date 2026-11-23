from .cidade import Cidade
from .jogador import Jogador


class Menu:
    """Menu principal do jogo: exibe opcoes, le a escolha e age sobre ela."""

    def __init__(self):
        self._em_execucao = True
        self._jogador = None  # ainda nao existe jogo iniciado
        self._cidade = None

    def executar(self):
        """Laco principal: repete exibir -> ler -> processar ate o jogador sair."""
        while self._em_execucao:
            self._exibir_opcoes()
            opcao = self._ler_opcao()
            self._processar_opcao(opcao)
        print("\nAte a proxima, nobre mercador!")

    def _iniciar_novo_jogo(self):
        """Cria um Jogador e uma Cidade de verdade, perguntando os nomes."""
        nome_jogador = input("Digite o nome do jogador: ").strip()
        nome_cidade = input("Digite o nome da cidade: ").strip()

        self._jogador = Jogador(nome_jogador)
        self._cidade = Cidade(nome_cidade, self._jogador)
        self._cidade.exibir_status()

    def _exibir_opcoes(self):
        """So imprime o menu. Nao le nada do teclado."""
        print()
        print("=" * 42)
        print(" BOLONHA E MILANO")
        print(" Um jogo de estrategia economica medieval")
        print("=" * 42)
        print("1 - Novo jogo")
        print("2 - Ver status da cidade")
        print("3 - Sobre o jogo")
        print("0 - Sair")

    def _ler_opcao(self):
        """Le uma linha e converte para int. Entrada invalida devolve -1."""
        try:
            return int(input("Escolha uma opcao: ").strip())
        except ValueError:
            return -1
        except EOFError:  # Ctrl+D / fim da entrada: sai sem travar
            return 0

    def _processar_opcao(self, opcao):
        """Decide a acao de acordo com a opcao lida."""
        if opcao == 1:
            self._iniciar_novo_jogo()
        elif opcao == 2:
            if self._cidade is None:
                print("\nNenhum jogo iniciado. Escolha '1 - Novo jogo' primeiro.")
            else:
                self._cidade.exibir_status()
        elif opcao == 3:
            self._exibir_sobre()
        elif opcao == 0:
            self._em_execucao = False
        else:
            print("\nOpcao invalida! Digite 1, 2, 3 ou 0.")

    def _exibir_sobre(self):
        """Imprime o texto que explica o jogo (so para a opcao 3)."""
        print()
        print("--- SOBRE O JOGO ---")
        print("Bolonha e Milano e um jogo de estrategia economica medieval.")
        print("Voce governa uma cidade italiana: administra florins, terras e")
        print("graos, cuida da populacao, cobra impostos e constroi defesas")
        print("para prosperar mais que seus rivais.")