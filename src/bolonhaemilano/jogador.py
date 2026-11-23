class Jogador:
    """Jogador do jogo: tem um nome e um titulo de nobreza."""

    def __init__(self, nome):
        self._nome = nome
        self._titulo = "Cavaleiro"  # titulo inicial

    def get_nome(self):
        return self._nome

    def get_titulo(self):
        return self._titulo

    def set_titulo(self, titulo):
        self._titulo = titulo