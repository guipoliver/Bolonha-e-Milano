class Jogador:
    """Jogador do jogo: tem um nome e um nivel de nobreza."""

    _TITULOS = ("Cavaleiro", "Barão", "Conde", "Marquês", "Duque", "Rei/Rainha")

    def __init__(self, nome):
        self._nome = nome
        self._nivel_titulo = 0

    def get_nome(self):
        return self._nome

    def get_titulo(self):
        return self._TITULOS[self._nivel_titulo]

    def get_nivel_titulo(self):
        return self._nivel_titulo

    def promover(self):
        if self.eh_monarca():
            return False
        self._nivel_titulo += 1
        return True

    def eh_monarca(self):
        return self._nivel_titulo == len(self._TITULOS) - 1
