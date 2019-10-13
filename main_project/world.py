from balloon import Balloon
from copy import copy, deepcopy
from threading import Lock


class Mundo:
    # Represents the world

    def __init__(self):
        self.all_balloons = {}
        self.has_balloon = False
        self.mutex = Lock()

    def set_balloon(self, name, position_x, position_y, height, area):
        """
        Change the information of a balloon
        :param name:
        :param position_x:
        :param position_y:
        :param height:
        :param area:
        """
        balloon = self.all_balloons.get(name)
        if balloon is not None:
            self.mutex.acquire()
            balloon.set_information(position_x, position_y, height, area)
            self.mutex.release()

    def set_invisible_balloon(self, name):
        """
        Set a balloon as out of vision
        :param name: Name of balloon
        """
        balloon = self.all_balloons.get(name)

        if balloon is not None:
            self.mutex.acquire()
            balloon.set_invisible()
            self.mutex.release()

    @property
    def all_balloons(self):
        self.mutex.acquire()
        all_balloons = deepcopy(self.all_balloons)
        self.mutex.release()
        return all_balloons

    def get_balloon(self, name):
        """
        Get the balloon of given name
        :param name: Name of the balloon
        :return: The balloon
        """
        self.mutex.acquire()
        balloon = copy(self.all_balloons.get(name))
        self.mutex.release()
        return balloon

    def init_all_balloons(self, all_names):
        """
        Make a dict with all the possible balloons
        :param all_names: List with all the names of possible balloons
        """
        for name in all_names:
            self.all_balloons[name] = Balloon(name)

    def __str__(self):
        text = ""
        for balloon in self.all_balloons.values():
            text += str(balloon) + '\n'
        return text
