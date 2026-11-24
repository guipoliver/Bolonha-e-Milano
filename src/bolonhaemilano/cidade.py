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
        self._taxa_imposto = 10          # configuracao (%), nao e recurso
        self._nivel_justica = "Moderada"  # configuracao, nao e recurso
        self._soldados = 0
        self._construcoes = 0

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

    def get_taxa_imposto(self):
        return self._taxa_imposto

    def get_nivel_justica(self):
        return self._nivel_justica

    def get_soldados(self):
        return self._soldados

    def get_construcoes(self):
        return self._construcoes

    # --- configuracoes de governo (getter/setter simples) ---
    def set_taxa_imposto(self, taxa):
        self._taxa_imposto = taxa

    def set_nivel_justica(self, nivel):
        self._nivel_justica = nivel

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