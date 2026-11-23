class Cidade:
    """Cidade governada por um Jogador (o dono), com seus recursos."""

    def __init__(self, nome, dono):
        self._nome = nome
        self._ano_atual = 1400
        self._dono = dono
        self._florins = 1000
        self._terras = 10000  # hectares
        self._graos = 500     # unidades
        self._servos = 200    # populacao

    # --- getters ---
    def get_nome(self):
        return self._nome

    def get_ano_atual(self):
        return self._ano_atual

    def get_dono(self):
        return self._dono

    def get_florins(self):
        return self._florins

    def get_terras(self):
        return self._terras

    def get_graos(self):
        return self._graos

    def get_servos(self):
        return self._servos

    # --- tempo ---
    def avancar_ano(self):
        """Incrementa o ano em 1 (so sera usado a partir da Etapa 7)."""
        self._ano_atual += 1

    # --- florins ---
    def adicionar_florins(self, quantidade):
        self._florins += quantidade

    def remover_florins(self, quantidade):
        """Remove florins. Devolve False (sem alterar nada) se nao houver saldo."""
        if quantidade < 0 or quantidade > self._florins:
            return False
        self._florins -= quantidade
        return True

    # --- terras ---
    def adicionar_terras(self, quantidade):
        self._terras += quantidade

    def remover_terras(self, quantidade):
        """Remove terras. Devolve False (sem alterar nada) se nao houver hectares."""
        if quantidade < 0 or quantidade > self._terras:
            return False
        self._terras -= quantidade
        return True

    # --- graos ---
    def adicionar_graos(self, quantidade):
        self._graos += quantidade

    def remover_graos(self, quantidade):
        """Remove graos. Devolve False (sem alterar nada) se nao houver estoque."""
        if quantidade < 0 or quantidade > self._graos:
            return False
        self._graos -= quantidade
        return True

    # --- servos ---
    def adicionar_servos(self, quantidade):
        self._servos += quantidade

    def remover_servos(self, quantidade):
        """Remove servos. Devolve False (sem alterar nada) se nao houver servos."""
        if quantidade < 0 or quantidade > self._servos:
            return False
        self._servos -= quantidade
        return True

    # --- status ---
    def exibir_status(self):
        """Imprime nome, governante, ano e os quatro recursos."""
        print()
        print("--- STATUS DA CIDADE ---")
        print(f"Cidade: {self._nome}")
        print(f"Governante: {self._dono.get_titulo()} {self._dono.get_nome()}")
        print(f"Ano atual: {self._ano_atual}")
        print(f"Florins: {self._florins}")
        print(f"Terras: {self._terras} hectares")
        print(f"Graos: {self._graos} unidades")
        print(f"Servos: {self._servos}")