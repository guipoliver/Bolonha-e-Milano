class Governo:
    """Arrecada impostos e define taxa e nivel de justica.

    Nao guarda nenhuma Cidade: ela chega sempre como parametro (dependencia).
    """

    _TAXA_MAXIMA = 50
    _MULTIPLICADOR_JUSTA = 0.8
    _MULTIPLICADOR_MODERADA = 1.0
    _MULTIPLICADOR_SEVERA = 1.3

    def arrecadar_impostos(self, cidade):
        """base = servos * taxa / 100, vezes o fator da justica. Devolve o arrecadado."""
        base = cidade.get_servos() * cidade.get_taxa_imposto() // 100
        multiplicador = self._multiplicador_para(cidade.get_nivel_justica())
        arrecadado = int(base * multiplicador)
        cidade.adicionar_florins(arrecadado)
        return arrecadado

    def definir_taxa_imposto(self, cidade, taxa):
        """Valida 0 a 50. Devolve False (sem alterar nada) se invalida."""
        if taxa < 0 or taxa > self._TAXA_MAXIMA:
            return False
        cidade.set_taxa_imposto(taxa)
        return True

    def definir_justica(self, cidade, nivel):
        """Valida Justa/Moderada/Severa. Devolve False se invalido."""
        if nivel not in ("Justa", "Moderada", "Severa"):
            return False
        cidade.set_nivel_justica(nivel)
        return True

    def _multiplicador_para(self, nivel):
        if nivel == "Justa":
            return self._MULTIPLICADOR_JUSTA
        if nivel == "Severa":
            return self._MULTIPLICADOR_SEVERA
        return self._MULTIPLICADOR_MODERADA