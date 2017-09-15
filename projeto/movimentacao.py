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

        if velLin > 0:
            sentido0 = 1
        else:
            sentido0 = -1
        sentido1 = -sentido0
        dutycicle = abs(velLin)

        self.pwm.setPWM(0, sentido0, dutycicle)
        self.pwm.setPWM(1, sentido1, dutycicle)

    def finalizar(self):
        self.pwm.pwmFim()