from .menu import Menu


def main():
    """Ponto de entrada: cria o Menu e delega a execucao a ele."""
    menu = Menu()
    menu.executar()


if __name__ == "__main__":
    main()