from .agricultura import Agricultura
from .cidade import Cidade
from .construcoes import Construcoes
from .governo import Governo
from .jogador import Jogador
from .mercado import Mercado
from .nobreza import Nobreza
from .partida import Partida


class Menu:
    """Menu principal do jogo: exibe opcoes, le a escolha e age sobre ela."""

    def __init__(self):
        self._em_execucao = True
        self._partida = None  # ainda nao existe jogo iniciado
        self._cidade = None
        self._mercado = Mercado()
        self._agricultura = Agricultura()
        self._governo = Governo()
        self._construcoes = Construcoes()
        self._nobreza = Nobreza()

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
        print("2 - Ver status da cidade")
        print("3 - Mercado")
        print("4 - Agricultura")
        print("5 - Governo")
        print("6 - Construcoes")
        if self._cidade is not None:
            print(f"Ano {self._partida.get_ano_atual()} | Vez de {self._cidade.get_dono().get_nome()} ({self._cidade.get_nome()})")
        print("7 - Encerrar turno")
        print("8 - Ver classificacao")
        print("9 - Sobre o jogo")
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
            self._exibir_status()
        elif opcao == 3:
            self._abrir_mercado()
        elif opcao == 4:
            self._abrir_agricultura()
        elif opcao == 5:
            self._abrir_governo()
        elif opcao == 6:
            self._abrir_construcoes()
        elif opcao == 7:
            self._encerrar_turno()
        elif opcao == 8:
            self._exibir_classificacao()
        elif opcao == 9:
            self._exibir_sobre()
        elif opcao == 0:
            self._em_execucao = False
        else:
            print("\nOpcao invalida! Digite 1, 2, 3, 4, 5, 6, 7, 8, 9 ou 0.")

    def _iniciar_novo_jogo(self):
        """Cadastra de 1 a 4 jogadores e inicia a partida pelo primeiro."""
        quantidade = self._ler_quantidade("Quantos jogadores (1 a 4)? ")
        if not 1 <= quantidade <= Partida.MAXIMO_JOGADORES:
            quantidade = 2
            print("Quantidade invalida. A partida tera 2 jogadores.")

        partida = Partida()
        nomes_cidades = ("Bolonha", "Milano", "Florença", "Veneza")
        try:
            for i in range(quantidade):
                nome = input(f"Nome do jogador {i + 1}: ").strip()
                partida.adicionar_cidade(Cidade(nomes_cidades[i], Jogador(nome)))
        except EOFError:
            return
        self._partida = partida
        self._cidade = partida.get_cidade_atual()
        self._cidade.exibir_status()

    def _exibir_status(self):
        """Mostra o status da cidade, ou avisa se nao ha jogo iniciado."""
        if self._cidade is None:
            print("\nNenhum jogo iniciado. Escolha '1 - Novo jogo' primeiro.")
        else:
            self._cidade.exibir_status()

    # ------------------------------------------------------------------
    # Mercado (Etapa 3)
    # ------------------------------------------------------------------
    def _abrir_mercado(self):
        """Submenu do mercado: laco que so termina com a opcao 0."""
        if self._cidade is None:
            print("\nNenhum jogo iniciado. Escolha '1 - Novo jogo' primeiro.")
            return

        no_mercado = True
        while no_mercado:
            print()
            print("--- MERCADO ---")
            print(f"Preco do grao: {self._mercado.get_preco_grao()} florins por unidade")
            print(f"Preco da terra: {self._mercado.get_preco_terra()} florins por hectare")
            print(f"Seus recursos -> Florins: {self._cidade.get_florins()} | "
                  f"Graos: {self._cidade.get_graos()} | "
                  f"Terras: {self._cidade.get_terras()}")
            print("1 - Comprar graos")
            print("2 - Vender graos")
            print("3 - Comprar terras")
            print("4 - Vender terras")
            print("0 - Voltar")

            opcao = self._ler_opcao()
            if opcao == 1:
                self._comprar_graos()
            elif opcao == 2:
                self._vender_graos()
            elif opcao == 3:
                self._comprar_terras()
            elif opcao == 4:
                self._vender_terras()
            elif opcao == 0:
                no_mercado = False
            else:
                print("\nOpcao invalida! Digite 1, 2, 3, 4 ou 0.")

    def _ler_quantidade(self, mensagem="Quantidade: "):
        """Le e valida um numero inteiro. Entrada invalida devolve -1."""
        try:
            return int(input(mensagem).strip())
        except (ValueError, EOFError):
            return -1

    def _comprar_graos(self):
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print("\nQuantidade invalida! Digite um numero maior que zero.")
        elif self._mercado.comprar_graos(self._cidade, quantidade):
            print(f"\nCompra realizada: {quantidade} graos.")
        else:
            print("\nFlorins insuficientes para essa compra.")

    def _vender_graos(self):
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print("\nQuantidade invalida! Digite um numero maior que zero.")
        elif self._mercado.vender_graos(self._cidade, quantidade):
            print(f"\nVenda realizada: {quantidade} graos.")
        else:
            print("\nGraos insuficientes para essa venda.")

    def _comprar_terras(self):
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print("\nQuantidade invalida! Digite um numero maior que zero.")
        elif self._mercado.comprar_terras(self._cidade, quantidade):
            print(f"\nCompra realizada: {quantidade} hectares.")
        else:
            print("\nFlorins insuficientes para essa compra.")

    def _vender_terras(self):
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print("\nQuantidade invalida! Digite um numero maior que zero.")
        elif self._mercado.vender_terras(self._cidade, quantidade):
            print(f"\nVenda realizada: {quantidade} hectares.")
        else:
            print("\nTerras insuficientes para essa venda.")

    # ------------------------------------------------------------------
    # Agricultura (Etapa 4)
    # ------------------------------------------------------------------
    def _abrir_agricultura(self):
        """Submenu da agricultura: laco que so termina com a opcao 0."""
        if self._cidade is None:
            print("\nNenhum jogo iniciado. Escolha '1 - Novo jogo' primeiro.")
            return

        na_agricultura = True
        while na_agricultura:
            print()
            print("--- AGRICULTURA ---")
            print(f"Terras: {self._cidade.get_terras()} hectares | "
                  f"Servos: {self._cidade.get_servos()} | "
                  f"Graos: {self._cidade.get_graos()}")
            print("1 - Colher (processar safra)")
            print("2 - Distribuir alimentos")
            print("0 - Voltar")

            opcao = self._ler_opcao()
            if opcao == 1:
                self._colher()
            elif opcao == 2:
                self._distribuir_alimentos()
            elif opcao == 0:
                na_agricultura = False
            else:
                print("\nOpcao invalida! Digite 1, 2 ou 0.")

    def _colher(self):
        """Delega a colheita para Agricultura e imprime o resultado."""
        graos_antes = self._cidade.get_graos()
        hectares = self._agricultura.processar_colheita(self._cidade)
        if hectares == -1:
            print("\nA colheita deste ano ja foi feita.")
        elif hectares == 0:
            print("\nNao foi possivel cultivar: faltam terras, servos ou graos para semear.")
        else:
            graos_depois = self._cidade.get_graos()
            print(f"\nColheita realizada! Hectares cultivados: {hectares}")
            print(f"Graos: {graos_antes} -> {graos_depois} ({graos_depois - graos_antes:+d})")

    def _distribuir_alimentos(self):
        """Delega a distribuicao para Agricultura e imprime o resultado."""
        percentual = self._ler_quantidade("Percentual de graos a distribuir (20 a 80): ")
        graos_antes = self._cidade.get_graos()
        servos_antes = self._cidade.get_servos()

        if not self._agricultura.distribuir_alimentos(self._cidade, percentual):
            print("\nPercentual invalido! Digite um valor entre 20 e 80.")
            return

        distribuido = graos_antes - self._cidade.get_graos()
        servos_agora = self._cidade.get_servos()
        variacao = servos_agora - servos_antes

        print(f"\nForam distribuidos {distribuido} graos a populacao.")
        if variacao > 0:
            print(f"A populacao cresceu: +{variacao} servos (agora {servos_agora}).")
        elif variacao < 0:
            print(f"Faltou comida! A populacao diminuiu: {variacao} servos (agora {servos_agora}).")
        else:
            print("A populacao ficou estavel.")

    # ------------------------------------------------------------------
    # Governo (Etapa 5)
    # ------------------------------------------------------------------
    def _abrir_governo(self):
        """Submenu do governo: laco que so termina com a opcao 0."""
        if self._cidade is None:
            print("\nNenhum jogo iniciado. Escolha '1 - Novo jogo' primeiro.")
            return

        no_governo = True
        while no_governo:
            print()
            print("--- GOVERNO ---")
            print(f"Florins: {self._cidade.get_florins()} | "
                  f"Taxa de imposto: {self._cidade.get_taxa_imposto()}% | "
                  f"Justica: {self._cidade.get_nivel_justica()}")
            print("1 - Arrecadar impostos")
            print("2 - Definir taxa de imposto")
            print("3 - Definir nivel de justica")
            print("0 - Voltar")

            opcao = self._ler_opcao()
            if opcao == 1:
                self._arrecadar_impostos()
            elif opcao == 2:
                self._definir_taxa_imposto()
            elif opcao == 3:
                self._definir_justica()
            elif opcao == 0:
                no_governo = False
            else:
                print("\nOpcao invalida! Digite 1, 2, 3 ou 0.")

    def _arrecadar_impostos(self):
        """Delega a arrecadacao para Governo e imprime o resultado."""
        florins_antes = self._cidade.get_florins()
        arrecadado = self._governo.arrecadar_impostos(self._cidade)
        if arrecadado == -1:
            print("\nOs impostos deste ano ja foram arrecadados.")
            return
        print(f"\nImpostos arrecadados: {arrecadado} florins.")
        print(f"Florins: {florins_antes} -> {self._cidade.get_florins()}")

    def _definir_taxa_imposto(self):
        taxa = self._ler_quantidade("Nova taxa de imposto (0 a 50): ")
        if self._governo.definir_taxa_imposto(self._cidade, taxa):
            print(f"\nTaxa de imposto definida: {taxa}%.")
        else:
            print("\nTaxa invalida! Digite um valor entre 0 e 50.")

    def _definir_justica(self):
        print("\n1 - Justa (impostos x0,8)")
        print("2 - Moderada (impostos x1,0)")
        print("3 - Severa (impostos x1,3)")
        escolha = self._ler_quantidade("Escolha o nivel de justica: ")
        nivel = {1: "Justa", 2: "Moderada", 3: "Severa"}.get(escolha, "")
        if self._governo.definir_justica(self._cidade, nivel):
            print(f"\nNivel de justica definido: {nivel}.")
        else:
            print("\nNivel invalido! Escolha 1, 2 ou 3.")

    # ------------------------------------------------------------------
    # Construcoes (Etapa 6)
    # ------------------------------------------------------------------
    def _abrir_construcoes(self):
        """Submenu de construcoes: laco que so termina com a opcao 0."""
        if self._cidade is None:
            print("\nNenhum jogo iniciado. Escolha '1 - Novo jogo' primeiro.")
            return

        na_construcoes = True
        while na_construcoes:
            print()
            print("--- CONSTRUCOES ---")
            print(f"Florins: {self._cidade.get_florins()} | "
                  f"Servos: {self._cidade.get_servos()} | "
                  f"Soldados: {self._cidade.get_soldados()} | "
                  f"Construcoes: {self._cidade.get_construcoes()}")
            print(f"Preco do soldado: {self._construcoes.get_preco_soldado()} florins + 1 servo")
            print(f"Preco da construcao: {self._construcoes.get_preco_construcao()} florins")
            print("1 - Recrutar soldados")
            print("2 - Construir")
            print("0 - Voltar")

            opcao = self._ler_opcao()
            if opcao == 1:
                self._recrutar_soldados()
            elif opcao == 2:
                self._construir()
            elif opcao == 0:
                na_construcoes = False
            else:
                print("\nOpcao invalida! Digite 1, 2 ou 0.")

    def _recrutar_soldados(self):
        """Delega o recrutamento para Construcoes e imprime o resultado."""
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print("\nQuantidade invalida! Digite um numero maior que zero.")
        elif self._construcoes.recrutar_soldados(self._cidade, quantidade):
            print(f"\nRecrutamento realizado: {quantidade} soldados.")
        else:
            print("\nRecursos insuficientes: confira seus florins e servos.")

    def _construir(self):
        """Delega a construcao para Construcoes e imprime o resultado."""
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print("\nQuantidade invalida! Digite um numero maior que zero.")
        elif self._construcoes.construir(self._cidade, quantidade):
            print(f"\nConstrucao realizada: {quantidade} edificio(s).")
        else:
            print("\nFlorins insuficientes para essa construcao.")

    # ------------------------------------------------------------------
    # Rodadas e nobreza (Etapa 7)
    # ------------------------------------------------------------------
    def _encerrar_turno(self):
        if self._partida is None:
            print("\nNenhum jogo iniciado. Escolha '1 - Novo jogo' primeiro.")
            return
        if self._partida.passar_turno():
            print(f"\nFim do ano {self._partida.get_ano_atual()}!")
            promovidas = self._partida.encerrar_ano(self._nobreza)
            for cidade in promovidas:
                dono = cidade.get_dono()
                print(f"Promocao: {dono.get_nome()} agora e {dono.get_titulo()}!")
            self._exibir_classificacao()
            if self._partida.terminou():
                self._encerrar_partida()
                return
        self._cidade = self._partida.get_cidade_atual()
        print(f"\nAgora e a vez de {self._cidade.get_dono().get_nome()} ({self._cidade.get_nome()}).")

    def _exibir_classificacao(self):
        if self._partida is None:
            print("\nNenhum jogo iniciado. Escolha '1 - Novo jogo' primeiro.")
            return
        print("\n--- CLASSIFICACAO ---")
        cidades = sorted(self._partida.get_cidades(), key=lambda cidade: (
            cidade.get_dono().get_nivel_titulo(), self._nobreza.calcular_prestigio(cidade)), reverse=True)
        for i, cidade in enumerate(cidades, 1):
            dono = cidade.get_dono()
            prestigio = self._nobreza.calcular_prestigio(cidade)
            necessario = self._nobreza.prestigio_para_proximo_titulo(dono)
            falta = "Titulo maximo" if necessario == -1 else f"Faltam {max(0, necessario - prestigio)} pontos para o proximo titulo"
            print(f"{i}. {cidade.get_nome()} | {dono.get_nome()} | {dono.get_titulo()} | Prestigio: {prestigio} | {falta}")

    def _encerrar_partida(self):
        vencedor = self._partida.determinar_vencedor(self._nobreza)
        print("\n--- FIM DA PARTIDA ---")
        print(f"Vencedor: {vencedor.get_dono().get_nome()} ({vencedor.get_nome()}) - {vencedor.get_dono().get_titulo()}")
        self._partida = None
        self._cidade = None

    # ------------------------------------------------------------------
    def _exibir_sobre(self):
        """Imprime o texto que explica o jogo (so para a opcao 9)."""
        print()
        print("--- SOBRE O JOGO ---")
        print("Bolonha e Milano e um jogo de estrategia economica medieval.")
        print("Voce governa uma cidade italiana: administra florins, terras e")
        print("graos, cuida da populacao, cobra impostos e constroi defesas")
        print("para prosperar mais que seus rivais.")
