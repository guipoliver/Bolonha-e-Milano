class Menu:
    """Menu principal do jogo: exibe opcoes, le a escolha e age sobre ela."""

    def __init__(self):
        self._em_execucao = True

    def executar(self):
        """Laco principal: repete exibir -> ler -> processar ate o jogador sair."""
        while self._em_execucao:
            self._exibir_opcoes()
            opcao = self._ler_opcao()
            self._processar_opcao(opcao)
        print("\nAte a proxima, nobre mercador!")

    def _exibir_opcoes(self):
        """So imprime o menu. Nao le nada do teclado."""
        print()
        print("=" * 42)
        print(" BOLONHA E MILANO")
        print(" Um jogo de estrategia economica medieval")
        print("=" * 42)
        print("1 - Novo jogo")
        print("2 - Sobre o jogo")
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
            print("\nO novo jogo sera implementado na Etapa 2.")
        elif opcao == 2:
            self._exibir_sobre()
        elif opcao == 0:
            self._em_execucao = False
        else:
            print("\nOpcao invalida! Digite 1, 2 ou 0.")

    def _exibir_sobre(self):
        """Imprime o texto que explica o jogo (so para a opcao 2)."""
        print()
        print("--- SOBRE O JOGO ---")
        print("Bolonha e Milano e um jogo de estrategia economica medieval.")
        print("Voce governa uma cidade italiana: administra florins, terras e")
        print("graos, cuida da populacao, cobra impostos e constroi defesas")
        print("para prosperar mais que seus rivais.")