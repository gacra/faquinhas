from pwm import PWM

class Movimentacao:

    def __init__(self):
        self.pwm = PWM()

    def mover(self, velAng, velLin):
        # type: (int, int) -> None
        """
Mover o robo com as velocidades passadas
        :param velAng: Velocidade angular (-100 a 100)
        :param VelLin: Velocidade linear (-100 a 100)
        """
        debug = "Movendo!!\n"
        debug += "Vel angular = " + str(velAng)
        debug += "Vel linear = " + str(velLin)
        print(debug)

        if velLin == 0:
            #Apenas rotacao (em relacao ao proprio eixo)
            if velAng > 0:
                sentido0 = 1
            else:
                sentido0 = -1
            sentido1 = -sentido0
            dutycicle0 = dutycicle1 = abs(velAng)
        else:
            #Rotacao e translacao ou somente translacao
            x = (2 * (abs(velLin / 100.0))) / (1 + (1 - abs(velAng / 100.0)))

            if velLin > 0:
                sentido0 = 1
            else:
                sentido0 = -1
            sentido1 = sentido0

            if x > 1.0:
                x = 1

            if velAng > 0:
                dutycicle0 = x
                dutycicle1 = (1 - abs(velAng / 100.0)) * x
            else:
                dutycicle0 = (1 - abs(velAng / 100.0)) * x
                dutycicle1 = x

            dutycicle0 = int(100*dutycicle0)
            dutycicle1 = int(100*dutycicle1)

        self.pwm.setPWM(0, sentido0, dutycicle0)
        self.pwm.setPWM(1, sentido1, dutycicle1)

    def finalizar(self):
        self.pwm.pwmFim()

if __name__ == '__main__':
    movimentacao = Movimentacao()

    while True:
        velAng = raw_input("VelAng: ")

        if velAng == "sair":
            break

        velLin = raw_input("VelLin: ")

        movimentacao.mover(int(velAng), int(velLin))

    movimentacao.finalizar()