from movimentacao import Movimentacao
from threading import Thread

class IA(Thread):
    '''Tomada de decisoes do sistema'''

    def __init__(self, mundo):
        self.listaBexiga = []
        self.distSonar = None
        self.mundo = mundo
        self.movimentacao = Movimentacao()
        Thread.__init__(self)

    def decisao(self):
        if self.mundo.atualizado == True:
            self.listaBexiga = self.mundo.listaBexiga
            bexiga = self.listaBexiga.get('red')
            if bexiga.visivel == True:
                (x, y) = bexiga.getPos()
                velAng = int(x*100)
                velLim = int((1-bexiga.altura)*100)
                self.movimentacao.mover(velAng, velLim)
            self.mundo.atualizado = False

    def run(self):
        """
Metodo a rodar na Thread
        :param self:
        """
        while True:
            self.decisao()