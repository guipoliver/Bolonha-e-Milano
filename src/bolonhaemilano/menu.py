from .agricultura import Agricultura
from .cidade import Cidade
from .construcoes import Construcoes
from .governo import Governo
from .jogador import Jogador
from .mercado import Mercado
from .nobreza import Nobreza
from .partida import Partida
from .interface import Interface
from .persistencia import Persistencia


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
        self._interface = Interface()
        self._persistencia = Persistencia()

    def executar(self):
        """Laco principal: repete exibir -> ler -> processar ate o jogador sair."""
        while self._em_execucao:
            self._exibir_opcoes()
            opcao = self._ler_opcao()
            self._processar_opcao(opcao)
            if self._em_execucao and opcao not in (3, 4, 5, 6):
                self._interface.pausar()
        print("\nAte a proxima, nobre mercador!")

    def _exibir_opcoes(self):
        """So imprime o menu. Nao le nada do teclado."""
        self._interface.tela("BOLONHA E MILANO", 'principal', self._cidade)
        if self._cidade is not None:
            print(self._interface.progresso(self._cidade, self._nobreza))
        print("Estrategia economica medieval | 1400-1410")
        print('-' * 60)
        print("1 - Novo jogo")
        print("2 - Ver status da cidade")
        print("3 - Mercado")
        print("4 - Agricultura")
        print("5 - Governo")
        print("6 - Construcoes")
        print("7 - Encerrar turno")
        print("8 - Ver classificacao")
        print("9 - Sobre o jogo")
        print("10 - Salvar partida")
        print("11 - Carregar partida")
        print("0 - Sair")

    def _ler_inteiro(self, mensagem, valor_eof=-1):
        """Le uma linha e converte para int. Entrada invalida devolve -1."""
        try:
            return int(input(mensagem).strip())
        except ValueError:
            return -1
        except EOFError:
            self._interface.desativar_interacao()
            return valor_eof

    def _ler_opcao(self):
        """Le a opcao; fim da entrada equivale a sair ou voltar."""
        return self._ler_inteiro("Escolha uma opcao: ", 0)

    def _exigir_jogo_em_andamento(self):
        """Devolve False e avisa se nao ha partida iniciada."""
        if self._partida is None:
            print(self._interface.colorir("\nNenhum jogo iniciado. Escolha '1 - Novo jogo' primeiro.", "vermelho"))
            return False
        return True

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
        elif opcao == 10:
            self._salvar_partida()
        elif opcao == 11:
            self._carregar_partida()
        elif opcao == 0:
            if self._cidade is None or not self._interface.eh_interativa() or self._interface.confirmar("Sair da partida? Salve antes para continuar depois."):
                self._em_execucao = False
        else:
            print(self._interface.colorir("\nOpcao invalida! Digite uma opcao de 0 a 11.", "vermelho"))

    def _iniciar_novo_jogo(self):
        """Cadastra de 1 a 4 jogadores e inicia a partida pelo primeiro."""
        if self._partida is not None and not self._interface.confirmar("Substituir a partida atual?"):
            return
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
        self._interface.tela("NOVA PARTIDA", "principal", self._cidade)
        self._cidade.exibir_status()

    def _exibir_status(self):
        """Mostra o status da cidade, ou avisa se nao ha jogo iniciado."""
        if self._exigir_jogo_em_andamento():
            self._interface.tela("STATUS DA CIDADE", "status", self._cidade, "azul")
            self._cidade.exibir_status()
            print(self._interface.progresso(self._cidade, self._nobreza))

    # ------------------------------------------------------------------
    # Mercado (Etapa 3)
    # ------------------------------------------------------------------
    def _abrir_mercado(self):
        """Submenu do mercado: laco que so termina com a opcao 0."""
        if not self._exigir_jogo_em_andamento():
            self._interface.pausar()
            return

        no_mercado = True
        while no_mercado:
            self._interface.tela("MERCADO", "mercado", self._cidade, "ouro")
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
                print(self._interface.colorir("\nOpcao invalida! Digite 1, 2, 3, 4 ou 0.", "vermelho"))
            if no_mercado:
                self._interface.pausar()


    def _ler_quantidade(self, mensagem="Quantidade: "):
        """Le e valida um numero inteiro. Entrada invalida devolve -1."""
        return self._ler_inteiro(mensagem)

    def _comprar_graos(self):
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print(self._interface.colorir("\nQuantidade invalida! Digite um numero maior que zero.", "vermelho"))
        elif self._mercado.comprar_graos(self._cidade, quantidade):
            print(self._interface.colorir(f"\nCompra realizada: {quantidade} graos.", "verde"))
        else:
            print(self._interface.colorir("\nFlorins insuficientes para essa compra.", "vermelho"))

    def _vender_graos(self):
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print(self._interface.colorir("\nQuantidade invalida! Digite um numero maior que zero.", "vermelho"))
        elif self._mercado.vender_graos(self._cidade, quantidade):
            print(self._interface.colorir(f"\nVenda realizada: {quantidade} graos.", "verde"))
        else:
            print(self._interface.colorir("\nGraos insuficientes para essa venda.", "vermelho"))

    def _comprar_terras(self):
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print(self._interface.colorir("\nQuantidade invalida! Digite um numero maior que zero.", "vermelho"))
        elif self._mercado.comprar_terras(self._cidade, quantidade):
            print(self._interface.colorir(f"\nCompra realizada: {quantidade} hectares.", "verde"))
        else:
            print(self._interface.colorir("\nFlorins insuficientes para essa compra.", "vermelho"))

    def _vender_terras(self):
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print(self._interface.colorir("\nQuantidade invalida! Digite um numero maior que zero.", "vermelho"))
        elif self._mercado.vender_terras(self._cidade, quantidade):
            print(self._interface.colorir(f"\nVenda realizada: {quantidade} hectares.", "verde"))
        else:
            print(self._interface.colorir("\nTerras insuficientes para essa venda.", "vermelho"))

    # ------------------------------------------------------------------
    # Agricultura (Etapa 4)
    # ------------------------------------------------------------------
    def _abrir_agricultura(self):
        """Submenu da agricultura: laco que so termina com a opcao 0."""
        if not self._exigir_jogo_em_andamento():
            self._interface.pausar()
            return

        na_agricultura = True
        while na_agricultura:
            self._interface.tela("AGRICULTURA", "agricultura", self._cidade, "verde")
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
                print(self._interface.colorir("\nOpcao invalida! Digite 1, 2 ou 0.", "vermelho"))
            if na_agricultura:
                self._interface.pausar()


    def _colher(self):
        """Delega a colheita para Agricultura e imprime o resultado."""
        graos_antes = self._cidade.get_graos()
        hectares = self._agricultura.processar_colheita(self._cidade)
        if hectares == -1:
            print(self._interface.colorir("\nA colheita deste ano ja foi feita.", "vermelho"))
        elif hectares == 0:
            print("\nNao foi possivel cultivar: faltam terras, servos ou graos para semear.")
        else:
            graos_depois = self._cidade.get_graos()
            print(self._interface.colorir(f"\nColheita realizada! Hectares cultivados: {hectares}", "verde"))
            print(f"Graos: {graos_antes} -> {graos_depois} ({graos_depois - graos_antes:+d})")

    def _distribuir_alimentos(self):
        """Delega a distribuicao para Agricultura e imprime o resultado."""
        percentual = self._ler_quantidade("Percentual de graos a distribuir (20 a 80): ")
        graos_antes = self._cidade.get_graos()
        servos_antes = self._cidade.get_servos()

        if not self._agricultura.distribuir_alimentos(self._cidade, percentual):
            print(self._interface.colorir("\nPercentual invalido! Digite um valor entre 20 e 80.", "vermelho"))
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
        if not self._exigir_jogo_em_andamento():
            self._interface.pausar()
            return

        no_governo = True
        while no_governo:
            self._interface.tela("GOVERNO", "governo", self._cidade, "azul")
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
                print(self._interface.colorir("\nOpcao invalida! Digite 1, 2, 3 ou 0.", "vermelho"))
            if no_governo:
                self._interface.pausar()


    def _arrecadar_impostos(self):
        """Delega a arrecadacao para Governo e imprime o resultado."""
        florins_antes = self._cidade.get_florins()
        arrecadado = self._governo.arrecadar_impostos(self._cidade)
        if arrecadado == -1:
            print(self._interface.colorir("\nOs impostos deste ano ja foram arrecadados.", "vermelho"))
            return
        print(self._interface.colorir(f"\nImpostos arrecadados: {arrecadado} florins.", "verde"))
        print(f"Florins: {florins_antes} -> {self._cidade.get_florins()}")

    def _definir_taxa_imposto(self):
        taxa = self._ler_quantidade("Nova taxa de imposto (0 a 50): ")
        if self._governo.definir_taxa_imposto(self._cidade, taxa):
            print(self._interface.colorir(f"\nTaxa de imposto definida: {taxa}%.", "verde"))
        else:
            print(self._interface.colorir("\nTaxa invalida! Digite um valor entre 0 e 50.", "vermelho"))

    def _definir_justica(self):
        print("\n1 - Justa (impostos x0,8)")
        print("2 - Moderada (impostos x1,0)")
        print("3 - Severa (impostos x1,3)")
        escolha = self._ler_quantidade("Escolha o nivel de justica: ")
        nivel = {1: "Justa", 2: "Moderada", 3: "Severa"}.get(escolha, "")
        if self._governo.definir_justica(self._cidade, nivel):
            print(self._interface.colorir(f"\nNivel de justica definido: {nivel}.", "verde"))
        else:
            print(self._interface.colorir("\nNivel invalido! Escolha 1, 2 ou 3.", "vermelho"))

    # ------------------------------------------------------------------
    # Construcoes (Etapa 6)
    # ------------------------------------------------------------------
    def _abrir_construcoes(self):
        """Submenu de construcoes: laco que so termina com a opcao 0."""
        if not self._exigir_jogo_em_andamento():
            self._interface.pausar()
            return

        na_construcoes = True
        while na_construcoes:
            self._interface.tela("CONSTRUCOES", "construcoes", self._cidade, "ouro")
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
                print(self._interface.colorir("\nOpcao invalida! Digite 1, 2 ou 0.", "vermelho"))
            if na_construcoes:
                self._interface.pausar()


    def _recrutar_soldados(self):
        """Delega o recrutamento para Construcoes e imprime o resultado."""
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print(self._interface.colorir("\nQuantidade invalida! Digite um numero maior que zero.", "vermelho"))
        elif self._construcoes.recrutar_soldados(self._cidade, quantidade):
            print(self._interface.colorir(f"\nRecrutamento realizado: {quantidade} soldados.", "verde"))
        else:
            print(self._interface.colorir("\nRecursos insuficientes: confira seus florins e servos.", "vermelho"))

    def _construir(self):
        """Delega a construcao para Construcoes e imprime o resultado."""
        quantidade = self._ler_quantidade()
        if quantidade <= 0:
            print(self._interface.colorir("\nQuantidade invalida! Digite um numero maior que zero.", "vermelho"))
        elif self._construcoes.construir(self._cidade, quantidade):
            print(self._interface.colorir(f"\nConstrucao realizada: {quantidade} edificio(s).", "verde"))
        else:
            print(self._interface.colorir("\nFlorins insuficientes para essa construcao.", "vermelho"))

    # ------------------------------------------------------------------
    # Rodadas e nobreza (Etapa 7)
    # ------------------------------------------------------------------
    def _encerrar_turno(self):
        if not self._exigir_jogo_em_andamento():
            return
        self._interface.arte("turno", "azul")
        if self._partida.passar_turno():
            print(f"\nFim do ano {self._partida.get_ano_atual()}!")
            promovidas = self._partida.encerrar_ano(self._nobreza)
            for cidade in promovidas:
                dono = cidade.get_dono()
                self._interface.arte("promocao")
                print(f"Promocao: {dono.get_nome()} agora e {dono.get_titulo()}!")
            self._exibir_classificacao()
            if self._partida.terminou():
                self._encerrar_partida()
                return
        self._cidade = self._partida.get_cidade_atual()
        print(f"\nAgora e a vez de {self._cidade.get_dono().get_nome()} ({self._cidade.get_nome()}).")

    def _exibir_classificacao(self):
        if not self._exigir_jogo_em_andamento():
            return
        self._interface.titulo("CLASSIFICACAO", "classificacao")
        cidades = sorted(self._partida.get_cidades(), key=lambda cidade: (
            cidade.get_dono().get_nivel_titulo(), self._nobreza.calcular_prestigio(cidade)), reverse=True)
        for i, cidade in enumerate(cidades, 1):
            dono = cidade.get_dono()
            print(self._interface.colorir(f"{i:02d}. {cidade.get_nome()} | {dono.get_nome()} | {dono.get_titulo()}", "ouro" if i == 1 else "azul"))
            print("    " + self._interface.progresso(cidade, self._nobreza))

    def _encerrar_partida(self):
        vencedor = self._partida.determinar_vencedor(self._nobreza)
        self._interface.titulo("FIM DA PARTIDA", "vitoria")
        print(f"Vencedor: {vencedor.get_dono().get_nome()} ({vencedor.get_nome()}) - {vencedor.get_dono().get_titulo()}")
        self._partida = None
        self._cidade = None

    # ------------------------------------------------------------------
    def _exibir_sobre(self):
        """Imprime o texto que explica o jogo (so para a opcao 9)."""
        self._interface.titulo("SOBRE O JOGO", "principal")
        print("Bolonha e Milano e um jogo de estrategia economica medieval.")
        print("Voce governa uma cidade italiana: administra florins, terras e")
        print("graos, cuida da populacao, cobra impostos e constroi defesas")
        print("para prosperar mais que seus rivais.")


    # ------------------------------------------------------------------
    # Salvamento (Bonus)
    # ------------------------------------------------------------------
    def _salvar_partida(self):
        if not self._exigir_jogo_em_andamento():
            return
        self._interface.arte('arquivo')
        try:
            self._persistencia.salvar(self._partida)
            print(self._interface.colorir('Partida salva em partida.json!', 'verde'))
        except (OSError, ValueError) as erro:
            print(self._interface.colorir(f'Nao foi possivel salvar: {erro}', 'vermelho'))

    def _carregar_partida(self):
        if self._partida is not None and not self._interface.confirmar('Substituir a partida atual pelo arquivo salvo?'):
            return
        self._interface.arte('arquivo')
        try:
            partida = self._persistencia.carregar()
        except (OSError, ValueError) as erro:
            print(self._interface.colorir(f'Nao foi possivel carregar: {erro}', 'vermelho'))
            return
        self._partida = partida
        self._cidade = partida.get_cidade_atual()
        print(self._interface.colorir('Partida carregada!', 'verde'))
        self._interface.cabecalho(self._cidade)
