class Nobreza:
    """Calcula o prestigio e verifica a promocao de um governante."""

    _PESO_CONSTRUCAO = 10
    _PESO_SOLDADO = 2
    _PESO_SERVO = 1
    _HECTARES_POR_PONTO = 100
    _PRESTIGIO_MINIMO = (0, 400, 550, 700, 850, 1000)

    def calcular_prestigio(self, cidade):
        return (cidade.get_construcoes() * self._PESO_CONSTRUCAO
                + cidade.get_soldados() * self._PESO_SOLDADO
                + cidade.get_servos() * self._PESO_SERVO
                + cidade.get_terras() // self._HECTARES_POR_PONTO)

    def prestigio_para_proximo_titulo(self, jogador):
        if jogador.eh_monarca():
            return -1
        return self._PRESTIGIO_MINIMO[jogador.get_nivel_titulo() + 1]

    def verificar_promocao(self, cidade):
        dono = cidade.get_dono()
        necessario = self.prestigio_para_proximo_titulo(dono)
        if necessario == -1 or self.calcular_prestigio(cidade) < necessario:
            return False
        return dono.promover()
