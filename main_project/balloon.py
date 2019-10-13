from copy import copy, deepcopy


class Balloon:
    # Balloon representation

    def __init__(self, name):
        self.name = name
        self.position_x = None
        self.position_y = None
        self.height = None
        self.area = None
        self.views_number = 0
        self.visible = False

    def set_information(self, position_x, position_y, height, area):
        """
        Change balloon's information
        :param position_x: Position x (1 a -1)
        :param position_y: Position y (1 a -1)
        :param height: Balloon's height
        :param area: Balloon's area
        """
        if self.views_number < 2:
            self.views_number += 1
        else:
            self.position_x = position_x
            self.position_y = position_y
            self.height = height
            self.area = area
            self.visible = True

    def set_invisible(self):
        """
        Used to indicate that the balloon is no longer visible
        """
        self.visible = False
        self.area = -1
        self.height = -1
        self.views_number = 0

    def get_position(self):
        return self.position_x, self.position_y

    def __str__(self):
        return ("Name: " + self.name + " X: " + str(self.position_x) +
                " Y: " + str(self.position_y) +
                " Height: " + str(self.height) +
                " Area: " + str(self.area) + " Visible: " + str(self.visible))


if __name__ == "__main__":
    balloon1 = Balloon("blue")
    balloon2 = copy(balloon1)

    balloon1.set_information(1, 2, 3, 4)
    balloon1.set_information(1, 2, 3, 4)
    balloon1.set_information(1, 2, 3, 4)

    print("Balloon 1: " + str(balloon1))
    print("Balloon 2: " + str(balloon2))

    all_balloons1 = [Balloon("red"), Balloon("yellow")]
    all_balloons2 = deepcopy(all_balloons1)
    all_balloons1[0].set_information(4, 3, 2, 1)
    all_balloons1[0].set_information(4, 3, 2, 1)
    all_balloons1[0].set_information(4, 3, 2, 1)

    print(all_balloons2[0])
    print(all_balloons1[0])
