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

    def __init__(self, position=[100,100], mass=1, parent=None, velocity=[0,0]):
        position = [p + random.randrange(-5,5,1) for p in position]
        self.timeCounter = {
                'after_birth':0,
                'after_child': 0
                }
        self.bio_state = {
                'isRoot': False, # ∞ mass
                'hasChildren': False,
                'size': 0,  # for both stems and berries
                'width': 0, # for both stems and berries
                'type':'stem',
                'color':'#FFFFFF'
            }
        self.dna = {
                "space_required_for_reproduction": 20,
                "time_before_reproduction": 40,
                "chargeMultiplier": 0.1
                } #TODO
        self.physics = {
                "velocity":velocity[:],
                "position":position[:],
                "mass": mass,
                "charge":0,
                }
        self.physics["position"] = position
        self.parent = parent
        # import pdb;pdb.set_trace() 

    def isReproductable(self):
        return self.timeCounter["after_birth"] == self.dna["time_before_reproduction"]

    def applyForce(self, force):
        # print(self.physics["mass"])
        # root doesn't move:
        # if self.parent:
        self.physics["velocity"][0] += force[0] / self.physics["mass"]
        self.physics["velocity"][1] += force[1] / self.physics["mass"]
        self.physics["position"][0] += self.physics["velocity"][0]
        self.physics["position"][1] += self.physics["velocity"][1]

    def develop(self):
        self.size = math.log10(self.timeCounter["after_birth"] + 2)
        self.physics["charge"] = self.dna["chargeMultiplier"] * \
            math.log10(self.timeCounter["after_birth"] + 2)

    def reproduce(self):
        childNumber = 2
        if self.parent:
            childNumber = 5
        return [Cell(
            position=self.physics["position"], 
            velocity=self.physics["velocity"], 
            parent=self
            ) for i in range(childNumber)]

    def getPosition(self):
        return self.physics["position"]

    def getCharge(self):
        return self.physics["charge"]


class Scene:
    cells = []
    # Потом доделать Параметры вьюпорта (проекция координат мира на экран)

    def __init__(self):
        self.cells.append(Cell(position=[300,300], mass=100))
        self.cells.append(Cell(position=[300,300], mass=50, parent=self.cells[0]))

    def render(self):
        for cell in self.cells:
            if cell.parent:
                beginPoint = cell.getPosition()
                endPoint = cell.parent.getPosition()
                #print (beginPoint, endPoint)
                arcade.draw_line(beginPoint[0], beginPoint[1], endPoint[0], endPoint[1], arcade.color.RED, 3)

    def develop(self):
        for i, cell in enumerate(self.cells):
            # physics =========================================================
            distMin = 1.0
            otherCells = [c for c in self.cells[i+1:]]
            for oCell in otherCells:
                distX = cell.getPosition()[0] - oCell.getPosition()[0]
                distY = cell.getPosition()[1] - oCell.getPosition()[1]
                distance = math.sqrt(distX**2 + distY**2)
                if abs(distance) < distMin:
                    distance = distMin
                force = (0.1 * cell.getCharge() * oCell.getCharge()) / distance**2
                forceX = (force * distX) / distance
                forceY = (force * distY) / distance
                cell.applyForce((forceX,forceY))
                oCell.applyForce((-forceX,-forceY))
                debugForceKoeff = 3000
                arcade.draw_line(cell.getPosition()[0],
                                 cell.getPosition()[1],
                                 cell.getPosition()[0]+forceX*debugForceKoeff,
                                 cell.getPosition()[1]+forceY*debugForceKoeff,
                                 arcade.color.BLACK, 0.5)
                arcade.draw_line(oCell.getPosition()[0],
                                 oCell.getPosition()[1],
                                 oCell.getPosition()[0]-forceX*debugForceKoeff,
                                 oCell.getPosition()[1]-forceY*debugForceKoeff,
                                 arcade.color.BLACK, 0.5)
            #growth
            cell.develop()
            #reproduce
            if cell.isReproductable():
                self.cells.extend(cell.reproduce())
            #increasing timer
            cell.timeCounter["after_birth"] += 1


    def coordsWorldToScreen(self):
        return 1;

scene = Scene()

# Size of the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


def on_draw(delta_time):
    arcade.start_render()
    scene.render()
    scene.develop()

def main():

    # Open up our window
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Bouncing Rectangle Example")
    arcade.set_background_color(arcade.color.WHITE)

    # Tell the computer to call the draw command at the specified interval.
    arcade.schedule(on_draw, 1/8)

    # Run the program
    arcade.run()


if __name__ == "__main__":
    main()
