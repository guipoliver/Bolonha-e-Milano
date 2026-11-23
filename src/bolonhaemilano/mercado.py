class Mercado:
    """Compra e vende graos e terras a precos fixos.

    Nao guarda nenhuma Cidade: ela chega sempre como parametro (dependencia).
    """

    _PRECO_GRAO = 2    # florins por unidade de grao
    _PRECO_TERRA = 20  # florins por hectare

    def get_preco_grao(self):
        return self._PRECO_GRAO

    def get_preco_terra(self):
        return self._PRECO_TERRA

    def comprar_graos(self, cidade, quantidade):
        if quantidade <= 0:
            return False
        custo = quantidade * self._PRECO_GRAO
        if not cidade.remover_florins(custo):
            return False
        cidade.adicionar_graos(quantidade)
        return True

    def vender_graos(self, cidade, quantidade):
        if quantidade <= 0:
            return False
        if not cidade.remover_graos(quantidade):
            return False
        receita = quantidade * self._PRECO_GRAO
        cidade.adicionar_florins(receita)
        return True

    def comprar_terras(self, cidade, quantidade):
        if quantidade <= 0:
            return False
        custo = quantidade * self._PRECO_TERRA
        if not cidade.remover_florins(custo):
            return False
        cidade.adicionar_terras(quantidade)
        return True

    def vender_terras(self, cidade, quantidade):
        if quantidade <= 0:
            return False
        if not cidade.remover_terras(quantidade):
            return False
        receita = quantidade * self._PRECO_TERRA
        cidade.adicionar_florins(receita)
        return True