"""
This simple animation example shows how to bounce a rectangle
on the screen.

It assumes a programmer knows how to create functions already.

It does not assume a programmer knows how to create classes. If you do know
how to create classes, see the starting template for a better example:

http://pythonhosted.org/arcade/examples/starting_template.html

Or look through the examples showing how to use Sprites.

A video walk-through of this example is available at:
https://vimeo.com/168063840
"""

import arcade
import math
import pprint
import random

class Cell:
    parent = None

    def __init__(self, position=[300,300], mass=1, parent=None, level=0, angle=0):
        self.children = []
        self.timeCounter = {
                'after_birth':0,
                'after_child': 0,
                }
        self.bioState = {
                'isRoot': False, # ∞ mass
                'hasChildren': False,
                'size': 0,  # for both stems and berries
                'width': 0, # for both stems and berries
                'type': 'stem',
                'color': '#FFFFFF',
                'level': level,
                'angle': angle,
            }
        self.dna = {
                "space_required_for_reproduction": 20,
                "time_before_reproduction": 50,
                "time_before_branching": 500,
                "chargeMultiplier": 10,
                "sizeMultiplier": 30,
                } #TODO
        self.physics = {
                "mass": mass,
                "charge": 0,
                "position": position,
                }
        self.parent = parent

    # def is(self):
        # if not self.parent:
            # return self.timeCounter["after_birth"] == 0
        # return self.timeCounter["after_birth"] == self.dna["time_before_reproduction"]

    def applyForce(self, force):
        # root doesn't move:
        # if self.parent:
        # self.physics["velocity"][0] += force[0] / self.physics["mass"]
        # self.physics["velocity"][1] += force[1] / self.physics["mass"]
        pass

    def develop(self):
        # if not self.parent:

        # import pdb;pdb.set_trace() 
        # if self.children:
            # for c in self.children:
                # c.develop()
        # move
        if self.parent:
            vector = [
                self.bioState["size"] * math.sin(math.radians(self.bioState["angle"])),
                self.bioState["size"] * math.cos(math.radians(self.bioState["angle"]))
                    ]
            self.physics["position"] = [b+v for b, v in zip(self.parent.physics["position"], vector)]
        #bio
        self.bioState["size"] = self.dna["sizeMultiplier"] * \
            math.log10(self.timeCounter["after_birth"]/5 + 1)
        self.physics["charge"] = self.dna["chargeMultiplier"] * \
            math.log10(self.timeCounter["after_birth"] + 1)
        #reproduce
        self.reproduce()
        # timing
        self.timeCounter["after_birth"] += 1
        # recursive developing children
        [c.develop() for c in self.children]

    def reproduceNumber(self):
        if self.bioState["level"] == 0:
            if self.timeCounter["after_birth"] == 0:
                return 5
        elif \
                self.bioState["level"] == 3 or \
                self.bioState["level"] == 9 or \
                self.bioState["level"] == 27 or \
                self.bioState["level"] == 81:
                # self.bioState["level"] == 32 or \
                # self.bioState["level"] == 64:
            if self.timeCounter["after_birth"] == self.dna["time_before_reproduction"]:
                return 3
        else:
            if self.timeCounter["after_birth"] == self.dna["time_before_reproduction"]:
                return 1
        return 0

    def reproduce(self):
        childNumber = self.reproduceNumber()
        self.children.extend([Cell(
            parent=self,
            angle=random.randrange(0,100000),
            level=self.bioState["level"]+1,
            ) for i in range(childNumber)])

    def render(self):
        if self.parent:
            beginPoint = self.parent.physics["position"]
            endPoint = self.physics["position"]
            print(self)
            print(beginPoint)
            print(endPoint)
            arcade.draw_line(beginPoint[0], beginPoint[1], 
                    endPoint[0], endPoint[1], 
                    arcade.color.RED, 
                    # 1)
                    1+int(self.bioState["size"]*4/self.dna["sizeMultiplier"]))
        [c.render() for c in self.children]

    # def getPosition(self):
        # return self.physics["position"]

    def getCharge(self):
        return self.physics["charge"]


class Scene:
    cells = []
    # Потом доделать Параметры вьюпорта (проекция координат мира на экран)

    def __init__(self):
        self.cells.append(Cell())
        # self.cells[0].children.append(Cell(mass=1, level=1, parent=self.cells[0], angle=45))
        # self.cells[0].children[0].children.append(Cell(mass=1, level=1, parent=self.cells[0].children[0], angle=-45))

    def render(self):
        [c.render() for c in self.cells]

    def develop(self):
        # for i, cell in enumerate(self.cells):
        for c in self.cells:
            c.develop()


    def coordsWorldToScreen(self):
        return 1;

scene = Scene()

# Size of the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


def on_draw(delta_time):
    arcade.start_render()
    scene.develop()
    scene.render()

def main():

    # Open up our window
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Bouncing Rectangle Example")
    arcade.set_background_color(arcade.color.WHITE)

    # Tell the computer to call the draw command at the specified interval.
    arcade.schedule(on_draw, 1/80)

    # Run the program
    arcade.run()


if __name__ == "__main__":
    main()
