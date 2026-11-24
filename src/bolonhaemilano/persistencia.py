import json
from pathlib import Path
from .cidade import Cidade
from .jogador import Jogador
from .partida import Partida


class Persistencia:
    """Salva e restaura uma partida JSON, sem bibliotecas externas."""

    _RECURSOS = ('florins', 'terras', 'graos', 'servos', 'soldados', 'construcoes')

    def __init__(self, caminho='partida.json'):
        self._caminho = Path(caminho)

    def salvar(self, partida):
        if partida is None or not partida.get_cidades() or partida.terminou():
            raise ValueError('Nao ha partida ativa para salvar.')
        cidades = []
        for cidade in partida.get_cidades():
            dono = cidade.get_dono()
            dados = {'nome': cidade.get_nome(), 'jogador': dono.get_nome(),
                     'nivel': dono.get_nivel_titulo(), 'ano': cidade.get_ano_atual(),
                     'taxa': cidade.get_taxa_imposto(), 'justica': cidade.get_nivel_justica(),
                     'colheita': cidade.is_colheita_feita(), 'impostos': cidade.is_impostos_arrecadados()}
            for recurso in self._RECURSOS:
                dados[recurso] = getattr(cidade, 'get_' + recurso)()
            cidades.append(dados)
        dados = {'versao': 1, 'vez': partida.get_cidades().index(partida.get_cidade_atual()), 'cidades': cidades}
        temporario = self._caminho.with_suffix(self._caminho.suffix + '.tmp')
        temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')
        temporario.replace(self._caminho)

    @staticmethod
    def _inteiro(valor, minimo, maximo=None):
        if type(valor) is not int or valor < minimo or (maximo is not None and valor > maximo):
            raise ValueError('Valor numerico invalido no arquivo.')
        return valor

    def carregar(self):
        try:
            dados = json.loads(self._caminho.read_text(encoding='utf-8'))
            if not isinstance(dados, dict) or dados.get('versao') != 1:
                raise ValueError('Versao de salvamento invalida.')
            registros = dados['cidades']
            if not isinstance(registros, list) or not 1 <= len(registros) <= Partida.MAXIMO_JOGADORES:
                raise ValueError('Quantidade de cidades invalida.')
            vez = self._inteiro(dados['vez'], 0, len(registros) - 1)
            partida = Partida()
            ano_comum = None
            nomes = set()
            for registro in registros:
                nome, jogador = registro['nome'], registro['jogador']
                if not isinstance(nome, str) or not isinstance(jogador, str) or nome in nomes:
                    raise ValueError('Nome de cidade ou jogador invalido.')
                nomes.add(nome)
                dono = Jogador(jogador)
                for _ in range(self._inteiro(registro['nivel'], 0, 4)):
                    dono.promover()
                cidade = Cidade(nome, dono)
                ano = self._inteiro(registro['ano'], 1400, partida.get_ano_final())
                if ano_comum is not None and ano != ano_comum:
                    raise ValueError('Cidades em anos diferentes.')
                ano_comum = ano
                for _ in range(ano - 1400):
                    cidade.avancar_ano()
                for recurso in self._RECURSOS:
                    valor = self._inteiro(registro[recurso], 0)
                    atual = getattr(cidade, 'get_' + recurso)()
                    if valor >= atual:
                        getattr(cidade, 'adicionar_' + recurso)(valor - atual)
                    else:
                        getattr(cidade, 'remover_' + recurso)(atual - valor)
                cidade.set_taxa_imposto(self._inteiro(registro['taxa'], 0, 50))
                if registro['justica'] not in ('Justa', 'Moderada', 'Severa'):
                    raise ValueError('Nivel de justica invalido.')
                cidade.set_nivel_justica(registro['justica'])
                if type(registro['colheita']) is not bool or type(registro['impostos']) is not bool:
                    raise ValueError('Indicador anual invalido.')
                if registro['colheita']:
                    cidade.marcar_colheita_feita()
                if registro['impostos']:
                    cidade.marcar_impostos_arrecadados()
                partida.adicionar_cidade(cidade)
            for _ in range(vez):
                partida.passar_turno()
            return partida
        except (KeyError, TypeError, AttributeError, IndexError) as erro:
            raise ValueError('Arquivo de partida invalido.') from erro
