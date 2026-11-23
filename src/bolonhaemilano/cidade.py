class Cidade:
    """Cidade governada por um Jogador (o dono)."""

    def __init__(self, nome, dono):
        self._nome = nome
        self._ano_atual = 1400
        self._dono = dono

    def avancar_ano(self):
        """Incrementa o ano em 1 (so sera usado a partir da Etapa 7)."""
        self._ano_atual += 1

    def exibir_status(self):
        """Imprime nome da cidade, governante e ano atual."""
        print()
        print("--- STATUS DA CIDADE ---")
        print(f"Cidade: {self._nome}")
        print(f"Governante: {self._dono.get_titulo()} {self._dono.get_nome()}")
        print(f"Ano atual: {self._ano_atual}")