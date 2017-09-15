from bexiga import Bexiga
from copy import copy, deepcopy
from threading import Lock

class Mundo:
    """Representacao do mundo"""

    def __init__(self):
        self.listaBexiga = {}
        self.distSonar = None
        self.atualizado = False
        self.mutex = Lock()

    @property
    def distSonar(self):
        return self.distSonar

    @distSonar.setter
    def distSonar(self, distSonar):
        # type: (float) -> None
        self.distSonar = distSonar

    def setBexiga(self, nome, x, y, altura, area):
        # type: (str, float, float, float, float) -> None
        """
Altera as informacoes de uma bexiga da lista
        :param nome:
        :param x:
        :param y:
        :param altura:
        :param area:
        """
        bexiga = self.listaBexiga.get(nome)
        if bexiga is not None:
            self.mutex.acquire()
            bexiga.setInfo(x, y, altura, area)
            self.mutex.release()

    def bexigaInvisivel(self, nome):
        """
Torna uma bexiga fora da visao
        :param nome: Nome da bexiga
        """
        bexiga = self.listaBexiga.get(nome)

        if bexiga is not None:
            self.mutex.acquire()
            bexiga.setInvisivel()
            self.mutex.release()

    @property
    def listaBexiga(self):
        # type: () -> Bexiga
        self.mutex.acquire()
        retorno =  deepcopy(self.listaBexiga)
        self.mutex.release()
        return retorno

    def getBexiga(self, nome):
        # type: (str) -> None
        """
Obtem a bexiga de nome especificado
        :param nome: Nome da bexiga que se deseja obter
        :return:
        """
        self.mutex.acquire()
        retorno = copy(self.listaBexiga.get(nome))
        self.mutex.release()
        return retorno

    def montaListaBexiga(self, nomes):
        # type: (list[str]) -> None
        """
Montar a lista com as bexigas disponiveis
        :param nomes: Lista com nome das bexigas disponiveis
        """
        for nome in nomes:
            self.listaBexiga[nome] = Bexiga(nome)

    def __str__(self):
        texto = ""
        for bexiga in self.listaBexiga.values():
            texto += str(bexiga) + '\n'
        return texto