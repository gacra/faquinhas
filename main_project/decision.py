from driver import Driver
from operator import attrgetter

import time

class DecisionMaker():
    # Makes the decisions

    def __init__(self, world):
        self.all_balloons = []
        self.world = world
        self.driver = Driver()
        self.current_state = States.WithoutBalloon
        self.pid = PID()
        self.with_balloon_counter = 0
        self.spin_counter = 0
        self.last_side = 1

    def run_towards_balloon(self, balloon):
        (position_x, position_y) = balloon.get_position()
        position_x = -position_x
        angular_speed = self.pid.iterate(position_x)
        if angular_speed > 9.09:
            angular_speed = 9.09

        height = balloon.height
        linear_speed = 0.9 - height
        if linear_speed > 0.8:
            linear_speed = 0.8
        elif linear_speed < 0.20:
            linear_speed = 0.20

        self.driver.move(angular_speed, linear_speed)

    def spin(self):
        if self.last_side == 1:
            angular_speed = 1.7
        else:
            angular_speed = -1.6
        self.driver.move(angular_speed, 0)
    
    def curve(self):
        if self.last_side == 1:
            angular_speed = -1
        else:
            angular_speed = 1
        self.driver.move(angular_speed, 0.15)

    def make_decision(self):

        self.all_balloons = self.world.all_balloons

        balloon = max(self.all_balloons.values(), key=attrgetter("area"))
        
        if self.current_state == States.WithoutBalloon:
            if balloon.visible is True:
                self.pid.reset()
                self.run_towards_balloon(balloon)
                self.with_balloon_counter = 1
                self.current_state = States.WithBalloon
                print("First time")
            else:
                self.spin()
                self.current_state = States.WithoutBalloon
                print("Without balloon")
        elif self.current_state == States.WithBalloon:
            if balloon.visivel is True:
                self.run_towards_balloon(balloon)
                if self.with_balloon_counter >= 10:
                    if balloon.position_x > 0:
                        self.last_side = -1
                    else:
                        self.last_side = 1
                self.with_balloon_counter += 1
                self.current_state = States.WithBalloon
                print("With balloon")
            else:
                if self.with_balloon_counter < 10:
                    self.with_balloon_counter = 10
                    self.curve()
                    self.spin_counter = 1
                    self.current_state = States.Spin
                    print("Spin")
                else:
                    self.spin()
                    self.current_state = States.WithoutBalloon
                    print("Without balloon")
        elif self.current_state == States.Spin:
            if balloon.visible is True:
                self.pid.reset()
                self.run_towards_balloon(balloon)
                self.current_state = States.WithBalloon
                print("With balloon*")
            else:
                if self.spin_counter < 20:
                    self.curve()
                    self.spin_counter += 1
                    self.current_state = States.Spin
                    print("Spin")
                if self.spin_counter >= 20:
                    self.spin()
                    self.current_state = States.WithoutBalloon
                    print("Without balloon")

    def finish(self):
        self.driver.finish()


class PID():
    def __init__(self):
        self.error_i = None
        self.previous_error = None
        self.previous_time = None
        self.kp = 1.4
        self.ki = 0.05
        self.kd = 0.5

    def reset(self):
        self.previous_error = None
        self.previous_time = None
        self.error_i = None

    def iterate(self, error):
        if self.previous_error is not None:
            current_time = time.clock()
            dt = current_time - self.previous_time
            self.previous_time = current_time
            diff = (error - self.previous_error) / dt
            self.error_i += error * dt
        else:
            self.error_i = 0
            diff = 0
            self.previous_time = time.clock()

        p_term = self.kp * error
        d_term = self.kd * diff
        i_term = self.ki * self.error_i

        # Limiting the integrator
        if i_term > 0.7:
            i_term = 0.7
        if i_term < -0.7:
            i_term = -0.7

        self.previous_error = error

        return p_term + d_term + i_term


class States:
    WithoutBalloon, Spin, WithBalloon = range(3)
