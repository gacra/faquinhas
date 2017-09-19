from copy import copy, deepcopy

class Bexiga:
    '''Representacao das bexigas'''

    def __init__(self, nome):
        self.nome = nome
        self.x = None
        self.y = None
        self.altura = None
        self.area = None
        self.numVis = 0
        self.visivel = False

    def setInfo(self, x, y, altura, area):
        """
Altera as informacoes da bexiga
        :param x: Posicao x (1 a -1)
        :param y: Posicao y (1 a -1)
        :param altura: Altura da bexiga
        :param area: Area da bexiga
        """
        if self.numVis < 2:
            self.numVis += 1
        else:
            self.x = x
            self.y = y
            self.altura = altura
            self.area = area
            self.visivel = True

    def setInvisivel(self):
        """
Usado para indicar que a bexiga nao eh mais visivel
        """
        self.visivel = False
        self.area = -1
        self.h = -1
        self.numVis = 0

    def getPos(self):
        return (self.x, self.y)

    def __str__(self):
        return "Nome: " + self.nome + " X: " + str(self.x) + " Y: " + str(self.y) + " Alt: " + str(self.altura) + " Area: " + str(self.area) + " Visivel: " + str(self.visivel)

if __name__ == "__main__":
    bexiga1 = Bexiga("azul")
    bexiga2 = copy(bexiga1)

    bexiga1.setInfo(1, 2, 3, 4)
    bexiga1.setInfo(1, 2, 3, 4)
    bexiga1.setInfo(1, 2, 3, 4)

    print("Bexiga 1: " + str(bexiga1))
    print("Bexiga 2: " + str(bexiga2))

    lista = [Bexiga("vermela"), Bexiga("amarela")]
    lista2 = deepcopy(lista)
    lista[0].setInfo(4, 3, 2, 1)
    lista[0].setInfo(4, 3, 2, 1)
    lista[0].setInfo(4, 3, 2, 1)

    print(lista2[0])
    print(lista[0])

