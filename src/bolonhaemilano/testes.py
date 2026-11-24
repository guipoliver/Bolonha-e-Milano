from .agricultura import Agricultura
from .cidade import Cidade
from .construcoes import Construcoes
from .governo import Governo
from .jogador import Jogador
from .mercado import Mercado
from .nobreza import Nobreza
from .partida import Partida


class Testes:
    """Testes automatizados das regras do jogo, sem bibliotecas externas."""

    _aprovados = 0
    _reprovados = 0

    @staticmethod
    def _verificar(descricao, condicao):
        if condicao:
            Testes._aprovados += 1
            print(f"[OK]    {descricao}")
        else:
            Testes._reprovados += 1
            print(f"[FALHA] {descricao}")

    @staticmethod
    def _nova_cidade():
        return Cidade("Bolonha", Jogador("Teste"))

    @staticmethod
    def _testar_cidade():
        print("\n-- Cidade --")
        cidade = Testes._nova_cidade()
        Testes._verificar("cidade nasce com 1000 florins", cidade.get_florins() == 1000)
        Testes._verificar("cidade nasce no ano 1400", cidade.get_ano_atual() == 1400)
        removeu = cidade.remover_florins(1001)
        Testes._verificar("remover florins acima do saldo devolve False", not removeu)
        Testes._verificar("... e nao altera o saldo", cidade.get_florins() == 1000)
        cidade.marcar_colheita_feita()
        cidade.marcar_impostos_arrecadados()
        cidade.avancar_ano()
        Testes._verificar("avancar_ano soma 1 ao ano", cidade.get_ano_atual() == 1401)
        Testes._verificar("avancar_ano libera colheita e impostos", not cidade.is_colheita_feita() and not cidade.is_impostos_arrecadados())

    @staticmethod
    def _testar_mercado():
        print("\n-- Mercado --")
        cidade = Testes._nova_cidade()
        mercado = Mercado()
        comprou = mercado.comprar_graos(cidade, 100)
        Testes._verificar("comprar 100 graos da certo", comprou)
        Testes._verificar("... e custa 200 florins", cidade.get_florins() == 800)
        Testes._verificar("... e soma 100 graos", cidade.get_graos() == 600)
        comprou = mercado.comprar_graos(cidade, -1)
        Testes._verificar("comprar quantidade negativa e recusado", not comprou and cidade.get_florins() == 800 and cidade.get_graos() == 600)
        comprou = mercado.comprar_graos(cidade, 401)
        Testes._verificar("comprar sem saldo e recusado", not comprou and cidade.get_florins() == 800 and cidade.get_graos() == 600)

    @staticmethod
    def _testar_agricultura():
        print("\n-- Agricultura --")
        cidade = Testes._nova_cidade()
        agricultura = Agricultura()
        hectares = agricultura.processar_colheita(cidade)
        Testes._verificar("primeira colheita cultiva 1000 hectares", hectares == 1000)
        Testes._verificar("... e deixa 2000 graos", cidade.get_graos() == 2000)
        hectares = agricultura.processar_colheita(cidade)
        Testes._verificar("segunda colheita no ano devolve -1", hectares == -1 and cidade.get_graos() == 2000)
        distribuiu = agricultura.distribuir_alimentos(cidade, 10)
        Testes._verificar("distribuir 10% e recusado", not distribuiu and cidade.get_graos() == 2000 and cidade.get_servos() == 200)

    @staticmethod
    def _testar_governo():
        print("\n-- Governo --")
        cidade = Testes._nova_cidade()
        governo = Governo()
        definiu = governo.definir_taxa_imposto(cidade, 60)
        Testes._verificar("taxa de 60% e recusada", not definiu and cidade.get_taxa_imposto() == 10)
        definiu = governo.definir_justica(cidade, "Branda")
        Testes._verificar("justica Branda e recusada", not definiu and cidade.get_nivel_justica() == "Moderada")
        governo.definir_justica(cidade, "Severa")
        arrecadado = governo.arrecadar_impostos(cidade)
        Testes._verificar("200 servos, 10%, Severa: arrecada 26 florins", arrecadado == 26 and cidade.get_florins() == 1026)
        arrecadado = governo.arrecadar_impostos(cidade)
        Testes._verificar("segunda arrecadacao no ano devolve -1", arrecadado == -1 and cidade.get_florins() == 1026)

    @staticmethod
    def _testar_construcoes():
        print("\n-- Construcoes --")
        cidade = Testes._nova_cidade()
        construcoes = Construcoes()
        # preparar, executar e verificar
        cidade.remover_servos(150)
        recrutou = construcoes.recrutar_soldados(cidade, 100)
        Testes._verificar("recrutar 100 com so 50 servos e recusado", not recrutou and cidade.get_servos() == 50 and cidade.get_soldados() == 0)
        Testes._verificar("... e NAO debita florins pela metade", cidade.get_florins() == 1000)
        construiu = construcoes.construir(cidade, 10)
        Testes._verificar("construir 10 da certo", construiu and cidade.get_construcoes() == 10)
        Testes._verificar("... e custa 200 florins", cidade.get_florins() == 800)

    @staticmethod
    def _testar_jogador_e_nobreza():
        print("\n-- Jogador e Nobreza --")
        cidade = Testes._nova_cidade()
        jogador = cidade.get_dono()
        nobreza = Nobreza()
        Testes._verificar("jogador comeca como Cavaleiro", jogador.get_titulo() == "Cavaleiro")
        Testes._verificar("prestigio inicial e 300", nobreza.calcular_prestigio(cidade) == 300)
        promoveu = nobreza.verificar_promocao(cidade)
        Testes._verificar("com prestigio 300 nao sobe de titulo", not promoveu)
        cidade.adicionar_construcoes(50)
        promoveu = nobreza.verificar_promocao(cidade)
        Testes._verificar("com 50 construcoes sobe para Barao", promoveu and jogador.get_titulo() == "Barão")
        Testes._verificar("sobe no maximo um titulo por chamada", jogador.get_nivel_titulo() == 1)
        for _ in range(4):
            jogador.promover()
        promoveu = jogador.promover()
        Testes._verificar("promover alem de Rei/Rainha e recusado", not promoveu and jogador.eh_monarca())

    @staticmethod
    def _testar_partida():
        print("\n-- Partida --")
        partida = Partida()
        nobreza = Nobreza()
        bolonha = Testes._nova_cidade()
        milano = Cidade("Milano", Jogador("Teste 2"))
        partida.adicionar_cidade(bolonha)
        partida.adicionar_cidade(milano)
        Testes._verificar("primeiro turno e de Bolonha", partida.get_cidade_atual() is bolonha)
        fim_ano = partida.passar_turno()
        Testes._verificar("passar turno de Bolonha NAO fecha o ano", not fim_ano and partida.get_ano_atual() == 1400)
        Testes._verificar("agora e a vez de Milano", partida.get_cidade_atual() is milano)
        fim_ano = partida.passar_turno()
        Testes._verificar("passar turno de Milano fecha o ano", fim_ano and partida.get_cidade_atual() is bolonha)
        milano.adicionar_construcoes(10)
        promovidas = partida.encerrar_ano(nobreza)
        Testes._verificar("encerrar_ano avanca todas as cidades", bolonha.get_ano_atual() == 1401 and milano.get_ano_atual() == 1401)
        Testes._verificar("partida ainda nao terminou em 1401", not partida.terminou())
        Testes._verificar("vencedor parcial e Milano (titulo mais alto)", milano in promovidas and partida.determinar_vencedor(nobreza) is milano)
        partida.adicionar_cidade(Cidade("Florença", Jogador("Teste 3")))
        partida.adicionar_cidade(Cidade("Veneza", Jogador("Teste 4")))
        adicionou = partida.adicionar_cidade(Cidade("Outra", Jogador("Teste 5")))
        Testes._verificar("quinta cidade e recusada (maximo 4)", not adicionou and len(partida.get_cidades()) == 4)

    @staticmethod
    def main():
        Testes._aprovados = 0
        Testes._reprovados = 0
        print("===== TESTES BOLONHA E MILANO =====")
        Testes._testar_cidade()
        Testes._testar_mercado()
        Testes._testar_agricultura()
        Testes._testar_governo()
        Testes._testar_construcoes()
        Testes._testar_jogador_e_nobreza()
        Testes._testar_partida()
        print(f"\nAprovados: {Testes._aprovados} | Reprovados: {Testes._reprovados}")
        if Testes._reprovados > 0:
            raise SystemExit(1)


if __name__ == "__main__":
    Testes.main()
