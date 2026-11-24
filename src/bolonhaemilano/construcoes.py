class Construcoes:
    """Recruta soldados e constroi edificios para uma Cidade.

    Nao guarda nenhuma Cidade: ela chega sempre como parametro (dependencia).
    """

    _PRECO_SOLDADO = 5          # florins por soldado
    _SERVOS_POR_SOLDADO = 1     # servos necessarios por soldado
    _PRECO_CONSTRUCAO = 20      # florins por construcao

    def recrutar_soldados(self, cidade, quantidade):
        """Recruta soldados. Valida florins e servos antes de alterar qualquer recurso."""
        if quantidade <= 0:
            return False

        custo = quantidade * self._PRECO_SOLDADO
        servos_necessarios = quantidade * self._SERVOS_POR_SOLDADO

        # Os dois recursos sao validados antes de qualquer debito.
        if (cidade.get_florins() < custo or
                cidade.get_servos() < servos_necessarios):
            return False

        cidade.remover_florins(custo)
        cidade.remover_servos(servos_necessarios)
        cidade.adicionar_soldados(quantidade)
        return True

    def construir(self, cidade, quantidade):
        """Constroi edificios. Devolve False se a quantidade ou o saldo forem insuficientes."""
        if quantidade <= 0:
            return False

        custo = quantidade * self._PRECO_CONSTRUCAO
        if not cidade.remover_florins(custo):
            return False

        cidade.adicionar_construcoes(quantidade)
        return True

    def get_preco_soldado(self):
        return self._PRECO_SOLDADO

    def get_preco_construcao(self):
        return self._PRECO_CONSTRUCAO