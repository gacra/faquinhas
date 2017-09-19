from movimentacao import Movimentacao
from threading import Thread

class IA(Thread):
    '''Tomada de decisoes do sistema'''

    def __init__(self, mundo):
        self.listaBexiga = []
        self.distSonar = None
        self.mundo = mundo
        self.movimentacao = Movimentacao()
        self.flag = False
        self.flag2 = False
        Thread.__init__(self)

    def decisao(self):
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

    def run(self):
        """
Metodo a rodar na Thread
        :param self:
        """
        while True:
            self.decisao()

    def finalizar(self):
        self.movimentacao.finalizar()
