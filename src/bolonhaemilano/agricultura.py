class Agricultura:
    """Processa a colheita do ano e a distribuicao de alimentos.

    Nao guarda nenhuma Cidade: ela chega sempre como parametro (dependencia).
    """

    _HECTARES_POR_SERVO = 5      # cada servo cultiva ate 5 hectares
    _RENDIMENTO_POR_HECTARE = 2  # cada hectare plantado rende 2 graos
    _SERVOS_POR_GRAO = 5         # 1 grao alimenta 5 servos (necessidade = servos / 5)
    _CRESCIMENTO_PERCENTUAL = 5  # populacao bem alimentada cresce 5%
    _PERCENTUAL_MINIMO = 20
    _PERCENTUAL_MAXIMO = 80

    def processar_colheita(self, cidade):
        """Planta, gasta sementes e produz graos novos. Devolve os hectares cultivados."""
        hectares = min(cidade.get_terras(), cidade.get_servos() * self._HECTARES_POR_SERVO)
        sementes = hectares // 2  # cada 2 hectares pedem 1 grao de semente

        # se faltar grao para semear, reduz hectares e sementes ao grao disponivel
        if sementes > cidade.get_graos():
            sementes = cidade.get_graos()
            hectares = sementes * 2

        cidade.remover_graos(sementes)
        producao = hectares * self._RENDIMENTO_POR_HECTARE
        cidade.adicionar_graos(producao)
        return hectares

    def distribuir_alimentos(self, cidade, percentual):
        """Distribui um percentual (20 a 80) dos graos. Devolve False se invalido."""
        if percentual < self._PERCENTUAL_MINIMO or percentual > self._PERCENTUAL_MAXIMO:
            return False

        alimento_distribuido = (cidade.get_graos() * percentual) // 100
        cidade.remover_graos(alimento_distribuido)

        necessidade = cidade.get_servos() // self._SERVOS_POR_GRAO
        if alimento_distribuido >= necessidade:
            crescimento = cidade.get_servos() * self._CRESCIMENTO_PERCENTUAL // 100
            cidade.adicionar_servos(crescimento)
        else:
            deficit = necessidade - alimento_distribuido
            cidade.remover_servos(min(deficit, cidade.get_servos()))
        return True