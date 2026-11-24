class Partida:
    """Guarda as cidades e controla os turnos, anos e o vencedor."""

    MAXIMO_JOGADORES = 4
    _ANO_FINAL = 1410

    def __init__(self):
        self._cidades = []
        self._indice_atual = 0

    def adicionar_cidade(self, cidade):
        if len(self._cidades) >= self.MAXIMO_JOGADORES:
            return False
        self._cidades.append(cidade)
        return True

    def get_cidades(self):
        return self._cidades.copy()

    def get_cidade_atual(self):
        if not self._cidades:
            return None
        return self._cidades[self._indice_atual]

    def get_ano_atual(self):
        return self._cidades[0].get_ano_atual() if self._cidades else 1400

    def get_ano_final(self):
        return self._ANO_FINAL

    def passar_turno(self):
        if not self._cidades or self.terminou():
            return False
        self._indice_atual += 1
        if self._indice_atual >= len(self._cidades):
            self._indice_atual = 0
            return True
        return False

    def encerrar_ano(self, nobreza):
        promovidas = []
        for cidade in self._cidades:
            cidade.avancar_ano()
            if nobreza.verificar_promocao(cidade):
                promovidas.append(cidade)
        return promovidas

    def terminou(self):
        return (self.get_ano_atual() > self._ANO_FINAL
                or any(cidade.get_dono().eh_monarca() for cidade in self._cidades))

    def determinar_vencedor(self, nobreza):
        if not self._cidades:
            return None
        return max(self._cidades, key=lambda cidade: (
            cidade.get_dono().get_nivel_titulo(), nobreza.calcular_prestigio(cidade)))
