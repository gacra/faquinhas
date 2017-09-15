class Sonar:
    '''Responsavel pelo tratamentos dos dados do sonar'''

    def __init__(self, maxDist, mundo):
        # type: (float, Mundo) -> None
        """
Inicializa o objeto sonar
        :param mundo: Objeto mundo
        :param maxDist: Maxima distancia que um objeto precisa estar para representar perigo
        """
        self.mundo = mundo
        self.maxDist = maxDist

    def update(self):
        """
Atualiza as informacoes no mundo a partir dos dados do sonar
        """
        pass

    def run(self):
        """
Metodo a rodar na Thread
        """
        pass