import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from .cidade import Cidade
from .jogador import Jogador
from .partida import Partida
from .nobreza import Nobreza
from .interface import Interface
from .persistencia import Persistencia
from .menu import Menu


class TestesBonus(unittest.TestCase):
    """Testes extras de persistencia e interface, sem alterar os 37 originais."""

    def setUp(self):
        self._pasta = tempfile.TemporaryDirectory()
        self.addCleanup(self._pasta.cleanup)
        self._arquivo = Path(self._pasta.name) / 'partida.json'
        self._persistencia = Persistencia(self._arquivo)
        self._partida = Partida()
        self._bolonha = Cidade('Bolonha', Jogador('Ana'))
        self._milano = Cidade('Milano', Jogador('Bruno'))
        self._partida.adicionar_cidade(self._bolonha)
        self._partida.adicionar_cidade(self._milano)

    def test_salvar_e_carregar_todos_os_dados(self):
        self._bolonha.adicionar_construcoes(14)
        self._bolonha.adicionar_soldados(3)
        self._bolonha.remover_servos(3)
        self._bolonha.remover_florins(295)
        self._bolonha.adicionar_graos(250)
        self._bolonha.adicionar_terras(5)
        self._bolonha.set_taxa_imposto(20)
        self._bolonha.set_nivel_justica('Severa')
        self._partida.encerrar_ano(Nobreza())
        self._bolonha.marcar_colheita_feita()
        self._milano.marcar_impostos_arrecadados()
        self._partida.passar_turno()
        self._persistencia.salvar(self._partida)
        original = json.loads(self._arquivo.read_text(encoding='utf-8'))
        carregada = self._persistencia.carregar()
        self.assertEqual(carregada.get_cidade_atual().get_nome(), 'Milano')
        self.assertEqual(carregada.get_ano_atual(), 1401)
        self._persistencia.salvar(carregada)
        self.assertEqual(original, json.loads(self._arquivo.read_text(encoding='utf-8')))

    def test_arquivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            self._persistencia.carregar()

    def test_json_corrompido(self):
        self._arquivo.write_text('{', encoding='utf-8')
        with self.assertRaises(ValueError):
            self._persistencia.carregar()

    def test_recusa_recurso_negativo(self):
        self._persistencia.salvar(self._partida)
        dados = json.loads(self._arquivo.read_text(encoding='utf-8'))
        dados['cidades'][0]['florins'] = -1
        self._arquivo.write_text(json.dumps(dados), encoding='utf-8')
        with self.assertRaises(ValueError):
            self._persistencia.carregar()

    def test_recusa_vez_invalida(self):
        self._persistencia.salvar(self._partida)
        dados = json.loads(self._arquivo.read_text(encoding='utf-8'))
        dados['vez'] = 2
        self._arquivo.write_text(json.dumps(dados), encoding='utf-8')
        with self.assertRaises(ValueError):
            self._persistencia.carregar()

    def test_recusa_salvar_sem_partida(self):
        with self.assertRaises(ValueError):
            self._persistencia.salvar(None)

    def test_barra_de_progresso(self):
        interface = Interface()
        self.assertIn('300/400', interface.progresso(self._bolonha, Nobreza()))
        self.assertIn('Faltam 100', interface.progresso(self._bolonha, Nobreza()))
        self._bolonha.adicionar_construcoes(100)
        self.assertIn('[####################]', interface.progresso(self._bolonha, Nobreza()))

    def test_falha_de_carregamento_preserva_partida(self):
        menu = Menu()
        menu._partida = self._partida
        menu._cidade = self._bolonha
        menu._persistencia = self._persistencia
        with patch.object(menu._interface, 'confirmar', return_value=True), patch('builtins.print'):
            menu._carregar_partida()
        self.assertIs(menu._partida, self._partida)
        self.assertIs(menu._cidade, self._bolonha)

    def test_pausa_e_limpeza_interativas(self):
        interface = Interface()
        interface._interativa = True
        with patch('builtins.input', return_value='') as entrada, patch('os.system') as limpar:
            interface.pausar()
            interface.limpar()
        entrada.assert_called_once()
        limpar.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=2)
