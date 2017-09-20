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
        #self.flag = False
        #self.flag2 = False
        self.estado = Estados.Inicial
        Thread.__init__(self)

    def decisao(self):

        self.listaBexiga = self.mundo.listaBexiga

        '''
        maxB = max(self.listaBexiga.values(), key=attrgetter("altura"))

        print(maxB)
        '''

        bexiga = self.listaBexiga.get('orange')

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

        #Girar rapido e voltar quando ver a bexiga -> essa parte de girar deu certo
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

        '''
        #Comecar girar rapido e desacelerar
        if bexiga.visivel == True:
            self.estado = Estados.ComBexiga
            (x, y) = bexiga.getPos()
            velAng = int(x * 100)
            velLim = int((1 - bexiga.altura) * 100)
            if velLim < 15 and velLim != 0:
                velLim = 15
                velAng = velAng * 1.5
            self.movimentacao.mover(-int(velAng / 2.5), int(velLim))
        else:
            if self.estado in [Estados.ComBexiga, Estados.Inicial]:
                self.movimentacao.mover(20, 0)
                self.estado = Estados.SemBexiga
                #time.sleep(0.01)
            elif self.estado == Estados.SemBexiga:
                self.movimentacao.mover(10, 0)
            else:
                self.movimentacao.mover(0, 0)
        '''
        #De ontem
        '''
        if self.mundo.atualizado == True:
            self.listaBexiga = self.mundo.listaBexiga
            bexiga = self.listaBexiga.get('orange')
            if self.flag2 == True:
                if bexiga.visivel == False:
                    self.movimentacao.mover(-14, 0)
                    #sleep(100)
                else:
                    self.flag2 = False
                return
            
            if bexiga.visivel == True:
                if self.flag == True:
                    self.flag2 = True
                    self.flag = False
                    return
                (x, y) = bexiga.getPos()
                velAng = int(x*100)
                velLim = int((1-bexiga.altura)*100)
                if velLim < 15 and velLim != 0:
                    velLim = 15
                    velAng = velAng * 1.5
                self.movimentacao.mover(-int(velAng/2.5), int(velLim))
            else:
                self.flag = True
                self.movimentacao.mover(20, 0)
            self.mundo.atualizado = False
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
    Inicial, SemBexiga, ComBexiga = range(3)
