from movimentacao import Movimentacao
import time
from operator import attrgetter

import time

class IA():
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

    def correrBexiga(self, bexiga):
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


    def decisao(self):

        self.listaBexiga = self.mundo.listaBexiga

        bexiga = max(self.listaBexiga.values(), key=attrgetter("area"))
        
        if bexiga.nome != 'pink' and bexiga.nome != 'orange':
            return

        #Se ve a bexiga
        if bexiga.visivel == True:

            #Se esta vendo pela primeira vez
            if self.estado == Estados.SemBexiga:
                self.pid.reset()
                self.movimentacao.mover(-1,0.15)
                time.sleep(0.6)
                self.estado = Estados.ComBexiga
                print("Reset PID")

            #Nao eh a primeira vez
            else:
                self.correrBexiga(bexiga)
                self.estado = Estados.ComBexiga
                print("Com bexiga")

        #Se nao ve a bexiga
        else:
            self.movimentacao.mover(1.7,0)
            self.estado = Estados.SemBexiga
            print("Sem bexiga")

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
        
        #print("Termo P :" + str(termo_p) + " Termo I: " + str(termo_i) + " Termo D: " +str(termo_d))

        self.erroAnterior = erro

        return termo_p + termo_d + termo_i


class Estados:
    Inicial, SemBexiga, PassouBexiga, ComBexiga = range(4)
