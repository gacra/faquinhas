from pwm import PWM


class Driver:

    def __init__(self):
        self.pwm = PWM()

    def move(self, angular_speed, linear_speed):
        """
        Move the robot with given speeds
        :param angular_speed: Angular speed (-100 a 100)
        :param linear_speed: Linear speed (-100 a 100)
        """

        robot_radius = 0.11
        max_speed = 1.0

        duty_cycle_0 = int(((-linear_speed - (
                    robot_radius * angular_speed)) / max_speed) * 100)
        duty_cycle_1 = int(((linear_speed - (
                    robot_radius * angular_speed)) / max_speed) * 100)

        if duty_cycle_0 > 0:
            orientation_0 = 1
        else:
            orientation_0 = -1

        if duty_cycle_1 > 0:
            orientation_1 = 1
        else:
            orientation_1 = -1

        self.pwm.setPWM(0, orientation_0, abs(duty_cycle_0))
        self.pwm.setPWM(1, orientation_1, abs(duty_cycle_1))


    def finish(self):
        self.pwm.pwmFim()


if __name__ == '__main__':
    driver = Driver()

    while True:
        angular_speed = raw_input("Angular speed: ")

        if angular_speed == "close":
            break

        linear_speed = raw_input("Linear speed: ")

        driver.move(float(angular_speed), float(linear_speed))

        print("--------------------")

    driver.finish()
