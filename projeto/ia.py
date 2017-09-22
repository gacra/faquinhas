from movimentacao import Movimentacao
from threading import Thread
import time
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
        self.pid = PID()
        Thread.__init__(self)

    def decisao(self):

        self.listaBexiga = self.mundo.listaBexiga

        bexiga = self.listaBexiga.get('orange')

        '''
        maxB = max(self.listaBexiga.values(), key=attrgetter("area"))

        print(maxB)
        '''
        '''
        #Teste nova girada
        if bexiga.visivel == True:
            if self.estado == Estados.SemBexiga:
                self.movimentacao.mover(10, 20)
                self.estado = Estados.PassouBexiga
                print("Passou bexiga")
                self.contador = 0
            elif self.estado == Estados.PassouBexiga:
                if self.contador < 1:
                    self.contador += 1
                    self.movimentacao.mover(10, 20)
                    self.estado = Estados.PassouBexiga
                    print("Passou bexiga")
                else:
                    (x, y) = bexiga.getPos()
                    velAng = int(x * 100)
                    velLim = int((1 - bexiga.altura) * 100)
                    if velLim < 15 and velLim != 0:
                        velLim = 15
                        velAng = velAng * 1.5
                    self.movimentacao.mover(-int(velAng / 4), int(velLim))
                    self.estado = Estados.ComBexiga
                    print("Correndo")
            elif self.estado in [Estados.Inicial, Estados.ComBexiga]:
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
                self.movimentacao.mover(10, 30)
                print("Passou bexiga")
        '''
        #Teste de correr ate a bexiga -> em andamento
        '''
        if bexiga.visivel == True:
            (x, y) = bexiga.getPos()
            x = -x
            velAng = int(x * 100)
            velLim = int((1 - bexiga.altura) * 100)
            if velLim < 15:
                velLim = 15
                velAng = velAng * 1.5
            if velAng < 0:
                if velAng < -28:
                    velAng = -28
                if velAng >-22:
                    velAng = -22
            elif velAng > 20:
                    velAng =20
            self.movimentacao.mover(int(velAng), 50)
            print("X: " +str(x)+ " Y: " + str(y) + " Vel Ang: " + str(int(velAng)) + " Vel Lim: " + str(50))
        else:
            self.movimentacao.mover(0,0)
        '''

        '''
        #teste correr PID -> bom pra caraio
        if bexiga.visivel == True:
            if self.estado == Estados.SemBexiga:
                self.pid.reset()
                self.estado = Estados.ComBexiga
                print("Reset PID")
                self.movimentacao.mover(-5,0)
                
                return
            (x, y) = bexiga.getPos()
            x = -x
            velAng = self.pid.iterar(x)
            if velAng > 9.09:
                velAng = 9.09
            altura = bexiga.altura
            velLin = 0.9 - altura
            if velLin > 0.8:
                velLin = 0.8
            elif velLin < 0.20:
                velLin = 0.20
            self.movimentacao.mover(velAng, velLin)
            print("VelLin: " + str(velLin) + " VelAng: " + str(velAng)) 
            print("Com bexiga")
        else:
            self.movimentacao.mover(0,0)
            self.estado = Estados.SemBexiga
            print("Sem bexiga")
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

class PID():
    def __init__(self):
        self.erroI = None
        self.erroAnterior = None
        self.tempoAnterior = None
        self.kp = 1.4
        self.ki = 0.05
        self.kd = 0.5

        
    def reset(self):
        self.erroAnterior = None
        self.tempoAnterior = None
        self.erroI = None

    def iterar(self, erro):
        if self.erroAnterior is not None:
            tempoAtual = time.clock()
            dt = tempoAtual - self.tempoAnterior
            self.tempoAnterior = tempoAtual
            diff = (erro-self.erroAnterior)/dt
            self.erroI += erro * dt
            #print("dt: " + str(dt)+ "Diff: " + str(diff) + "ErroI :" + str(self.erroI))
        else:
            self.erroI = 0
            diff = 0
            self.tempoAnterior = time.clock()

        termo_p = self.kp * erro
        termo_d = self.kd * diff
        termo_i = self.ki * self.erroI
        '''
        LIMITANDO TERMO DO ITNEGRADOR
        '''
        
        if termo_i > 0.7:
            termo_i = 0.7
        if termo_i < -0.7:
            termo_i = -0.7
        
        
        print("Termo P :" + str(termo_p) + " Termo I: " + str(termo_i) + " Termo D: " +str(termo_d))
        #print("P: " + str(termo_p) + "I: " + str(termo_i) + "D: " + str(termo_d))

        self.erroAnterior = erro

        return termo_p + termo_d + termo_i


class Estados:
    Inicial, SemBexiga, PassouBexiga, ComBexiga = range(4)
