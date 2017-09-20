from movimentacao import Movimentacao
from threading import Thread
from operator import attrgetter

import time

class IA(Thread):
    '''Tomada de decisoes do sistema'''

    def __init__(self, corAmiga, mundo):
        self.listaBexiga = []
        self.distSonar = None
        self.corAmiga = corAmiga
        self.mundo = mundo
        self.movimentacao = Movimentacao()
        self.contador = 0
        self.estado = Estados.Inicial
        Thread.__init__(self)

    def decisao(self):

        self.listaBexiga = self.mundo.listaBexiga

        bexiga = self.listaBexiga.get('orange')

        '''
        maxB = max(self.listaBexiga.values(), key=attrgetter("area"))

        print(maxB)
        '''

        #Teste nova girada
        if bexiga.visivel == True:
            if self.estado == Estados.SemBexiga:
                self.movimentacao.mover(-20, 20)
                self.estado = Estados.PassouBexiga
                print("Passou bexiga")
            if self.estado in [Estados.Inicial, Estados.PassouBexiga, Estados.ComBexiga]:
                (x, y) = bexiga.getPos()
                velAng = int(x * 100)
                velLim = int((1 - bexiga.altura) * 100)
                if velLim < 15 and velLim != 0:
                    velLim = 15
                    velAng = velAng * 1.5
                self.movimentacao.mover(-int(velAng / 4), int(velLim))
                self.estado = Estados.ComBexiga
                print("Correndo")

        else:
            if self.estado in [Estados.Inicial, Estados.ComBexiga, Estados.SemBexiga]:
                self.movimentacao.mover(20, 0)
                self.estado = Estados.SemBexiga
                print("Girando")
            elif self.estado == Estados.PassouBexiga:
                self.movimentacao.mover(-20, 20)
                print("Passou bexiga")

        #Teste de correr ate a bexiga -> em andamento
        '''
        if bexiga.visivel == True:
            (x, y) = bexiga.getPos()
            velAng = int(x * 100)
            velLim = int((1 - bexiga.altura) * 100)
            if velLim < 15:
                velLim = 15
                velAng = velAng * 1.5
            if velAng > 20:
                velAng = 20
            self.movimentacao.mover(-int(velAng), int(velLim))
            print("X: " +str(x)+ " Y: " + str(y) + " Vel Ang: " + str(-int(velAng / 4)) + " Vel Lim: " + str(int(velLim)))
        else:
            self.movimentacao.mover(0,0)
        '''

        # Girar rapido e voltar quando ver a bexiga -> essa parte de girar deu certo
        '''
        if bexiga.visivel == True:
            if self.estado == Estados.SemBexiga:
                self.movimentacao.mover(-20, 0)
                time.sleep(0.40)
                self.movimentacao.mover(0,0)
                time.sleep(0.01)
                self.estado = Estados.ComBexiga
                print("Ao contrario")
            elif self.estado in [Estados.ComBexiga, Estados.Inicial]:
                (x, y) = bexiga.getPos()
                velAng = int(x * 100)
                velLim = int((1 - bexiga.altura) * 100)
                if velLim < 15 and velLim != 0:
                    velLim = 15
                    velAng = velAng * 1.5
                self.movimentacao.mover(-int(velAng / 4), int(velLim))
                print("Correndo")
            else:
                self.movimentacao.mover(0, 0)
        else:
            self.movimentacao.mover(20, 0)
            self.estado = Estados.SemBexiga
            print("Girando")
        '''
    def run(self):
        """
Metodo a rodar na Thread
        :param self:
        """
        while True:
            self.decisao()

    def finalizar(self):
        self.movimentacao.finalizar()

class Estados:
    Inicial, SemBexiga, PassouBexiga, ComBexiga = range(4)
