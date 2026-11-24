import os
import sys
from .artes import ARTES


class Interface:
    """Apresentacao do terminal; nao modifica os recursos do jogo."""

    _CORES = {'ouro': '33', 'verde': '32', 'azul': '36', 'vermelho': '31'}

    def __init__(self):
        self._interativa = sys.stdin.isatty() and sys.stdout.isatty()
        self._cores = self._interativa and 'NO_COLOR' not in os.environ and os.environ.get('TERM') != 'dumb'
        if self._cores and os.name == 'nt':
            # Habilita sequencias ANSI no console Windows, quando disponivel.
            os.system('')

    def eh_interativa(self):
        return self._interativa

    def desativar_interacao(self):
        self._interativa = False
        self._cores = False

    def colorir(self, texto, cor='ouro'):
        if not self._cores:
            return texto
        return f'\033[{self._CORES.get(cor, "33")}m{texto}\033[0m'

    def limpar(self):
        if self._interativa:
            os.system('cls' if os.name == 'nt' else 'clear')

    def pausar(self):
        if self._interativa:
            try:
                input('\nPressione ENTER para continuar...')
            except EOFError:
                pass

    def confirmar(self, mensagem):
        try:
            return input(mensagem + ' [s/N]: ').strip().lower() in ('s', 'sim')
        except EOFError:
            return False

    def arte(self, chave, cor='ouro'):
        print(self.colorir(ARTES.get(chave, ''), cor))

    def titulo(self, texto, chave, cor='ouro'):
        self.arte(chave, cor)
        print(self.colorir('=' * 60, cor))
        print(self.colorir(texto.center(60), cor))
        print(self.colorir('=' * 60, cor))

    def cabecalho(self, cidade):
        if cidade is None:
            print('Nenhuma partida em andamento.')
            return
        dono = cidade.get_dono()
        print(self.colorir(f'ANO {cidade.get_ano_atual()} | {cidade.get_nome()} | {dono.get_titulo()} {dono.get_nome()}', 'ouro'))
        print(f'Florins: {cidade.get_florins()} | Graos: {cidade.get_graos()} | Terras: {cidade.get_terras()}')
        print(f'Servos: {cidade.get_servos()} | Soldados: {cidade.get_soldados()} | Construcoes: {cidade.get_construcoes()}')
        colheita = 'feita' if cidade.is_colheita_feita() else 'disponivel'
        impostos = 'feitos' if cidade.is_impostos_arrecadados() else 'disponiveis'
        print(f'Colheita: {colheita} | Impostos: {impostos}')
        print('-' * 60)

    def tela(self, texto, chave, cidade=None, cor='ouro'):
        self.limpar()
        self.titulo(texto, chave, cor)
        self.cabecalho(cidade)

    def progresso(self, cidade, nobreza):
        prestigio = nobreza.calcular_prestigio(cidade)
        meta = nobreza.prestigio_para_proximo_titulo(cidade.get_dono())
        if meta == -1:
            return f'[####################] {prestigio} pontos | Titulo maximo'
        anterior = (0, 400, 550, 700, 850, 1000)[cidade.get_dono().get_nivel_titulo()]
        partes = max(0, min(20, (prestigio - anterior) * 20 // (meta - anterior)))
        barra = '#' * partes + '.' * (20 - partes)
        return f'[{barra}] {prestigio}/{meta} | Faltam {max(0, meta - prestigio)} pontos'
