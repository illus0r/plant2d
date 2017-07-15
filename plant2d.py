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

    def __init__(self, position=[100.0,100.0], mass=1, parent=None, velocity=[0.0,0.0]):
        if parent:
            position = [p + random.gauss(0,1) for p in position]
        self.timeCounter = {
                'after_birth':0,
                'after_child': 0,
                }
        self.bioState = {
                'isRoot': False, # ∞ mass
                'hasChildren': False,
                'size': 0,  # for both stems and berries
                'width': 0, # for both stems and berries
                'type':'stem',
                'color':'#FFFFFF',
            }
        self.dna = {
                "space_required_for_reproduction": 20,
                "time_before_reproduction": 50,
                "time_before_branching": 500,
                "chargeMultiplier": 10,
                "sizeMultiplier": 10,
                } #TODO
        self.physics = {
                "velocity":velocity[:],
                "position":position[:],
                "mass": mass,
                "charge": 0,
                }
        self.physics["position"] = position
        self.parent = parent
        # import pdb;pdb.set_trace() 

    # def is(self):
        # if not self.parent:
            # return self.timeCounter["after_birth"] == 0
        # return self.timeCounter["after_birth"] == self.dna["time_before_reproduction"]

    def applyForce(self, force):
        # root doesn't move:
        # if self.parent:
        self.physics["velocity"][0] += force[0] / self.physics["mass"]
        self.physics["velocity"][1] += force[1] / self.physics["mass"]

    def develop(self):
        # physics
        friction = 0.95
        self.physics["position"][0] += self.physics["velocity"][0]
        self.physics["position"][1] += self.physics["velocity"][1]
        self.physics["velocity"] = [v*friction for v in self.physics["velocity"]]
        #bio
        self.bioState["size"] = self.dna["sizeMultiplier"] * \
            math.log10(self.timeCounter["after_birth"]/5 + 1)
        self.physics["charge"] = self.dna["chargeMultiplier"] * \
            math.log10(self.timeCounter["after_birth"] + 1)

    def reproduceNumber(self):
        if not self.parent:
            if self.timeCounter["after_birth"] == 0:
                return 5
        if self.timeCounter["after_birth"] == self.dna["time_before_branching"]:
            return 2
        elif self.timeCounter["after_birth"] == self.dna["time_before_reproduction"]:
            return 1
        else:
            return 0

    def reproduce(self):
        childNumber = self.reproduceNumber()
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
        self.cells.append(Cell(position=[300,300], mass=1000000000))

    def render(self):
        for cell in self.cells:
            if cell.parent:
                beginPoint = cell.getPosition()
                endPoint = cell.parent.getPosition()
                #print (beginPoint, endPoint)
                arcade.draw_line(beginPoint[0], beginPoint[1], 
                        endPoint[0], endPoint[1], 
                        arcade.color.RED, 
                        1)
                        # 1+int(cell.bioState["size"]*4/cell.dna["sizeMultiplier"]))

    def develop(self):
        for i, cell in enumerate(self.cells):
            # physics =========================================================
            distMin = 1.0
            centerCharge = 5
            junctureStrength = 0.1
            # electric --------------------------------------------------------
            distX = cell.getPosition()[0] - 300
            distY = cell.getPosition()[1] - 300
            distance = math.sqrt(distX**2 + distY**2)
            if abs(distance) < distMin:
                distance = distMin
            force = (0.1 * cell.getCharge() * centerCharge) / distance
            forceX = (force * distX) / distance
            forceY = (force * distY) / distance
            cell.applyForce((forceX,forceY))
            # junction --------------------------------------------------------
            if cell.parent:
                distX = cell.getPosition()[0] - cell.parent.getPosition()[0]
                distY = cell.getPosition()[1] - cell.parent.getPosition()[1]
                distance = math.sqrt(distX**2 + distY**2)
                if abs(distance) < distMin:
                    distance = distMin
                force = -junctureStrength * (distance - cell.bioState["size"])
                forceX = (force * distX) / distance
                forceY = (force * distY) / distance
                forceParentX = -(force * distX) / distance
                forceParentY = -(force * distY) / distance
                cell.applyForce((forceX,forceY))
                cell.parent.applyForce((forceParentX,forceParentY))
            # collisions ------------------------------------------------------
            radiusSizeRatio = 1 # 0.5 → half size
            collisionStrength = 0.01
            otherCells = [c for c in self.cells[i+1:]]
            radius = cell.bioState["size"] * radiusSizeRatio
            for j, oCell in enumerate(otherCells):
                if oCell != cell.parent:
                    oRadius = oCell.bioState["size"] * radiusSizeRatio
                    if oRadius<radius:
                        radius = oRadius
                    # print(radius)
                    distX = cell.getPosition()[0] - oCell.getPosition()[0]
                    distXAbs = abs(distX)
                    if distXAbs < radius:
                        distY = cell.getPosition()[1] - oCell.getPosition()[1]
                        distYAbs = abs(distY)
                        if distYAbs < radius:
                            # print(i, i+1+j)
                            # print("DistX, DistY: ", distX, distY)
                            forceX = (distX/distXAbs) * \
                                    (radius - distXAbs) * collisionStrength
                            forceY = (distY/distYAbs) * \
                                    (radius - distYAbs) * collisionStrength
                            cell.applyForce((forceX,forceY))
                            oCell.applyForce((-forceX,-forceY))
                        # else:
                            # print("too far Y")
                    # else:
                        # print("too far X")
                else:
                    print("parent")
                debugForceKoeff = 300
                # arcade.draw_line(cell.getPosition()[0],
                                 # cell.getPosition()[1],
                                 # cell.getPosition()[0]+forceX*debugForceKoeff,
                                 # cell.getPosition()[1]+forceY*debugForceKoeff,
                                 # arcade.color.BLACK, 0.5)
                # arcade.draw_line(oCell.getPosition()[0],
                                 # oCell.getPosition()[1],
                                 # oCell.getPosition()[0]-forceX*debugForceKoeff,
                                 # oCell.getPosition()[1]-forceY*debugForceKoeff,
                                 # arcade.color.BLACK, 0.5)

            # # electric force
            # debugForceKoeff = 3000
            # arcade.draw_line(cell.getPosition()[0],
                             # cell.getPosition()[1],
                             # cell.getPosition()[0]+forceX*debugForceKoeff,
                             # cell.getPosition()[1]+forceY*debugForceKoeff,
                             # arcade.color.BLACK, 0.5)

            # otherCells = [c for c in self.cells[i+1:]]
            # for oCell in otherCells:
                # distX = cell.getPosition()[0] - oCell.getPosition()[0]
                # distY = cell.getPosition()[1] - oCell.getPosition()[1]
                # distance = math.sqrt(distX**2 + distY**2)
                # if abs(distance) < distMin:
                    # distance = distMin
                # force = (0.1 * cell.getCharge() * oCell.getCharge()) / distance**2
                # forceX = (force * distX) / distance
                # forceY = (force * distY) / distance
                # cell.applyForce((forceX,forceY))
                # oCell.applyForce((-forceX,-forceY))
                # debugForceKoeff = 3000
                # arcade.draw_line(cell.getPosition()[0],
                                 # cell.getPosition()[1],
                                 # cell.getPosition()[0]+forceX*debugForceKoeff,
                                 # cell.getPosition()[1]+forceY*debugForceKoeff,
                                 # arcade.color.BLACK, 0.5)
                # arcade.draw_line(oCell.getPosition()[0],
                                 # oCell.getPosition()[1],
                                 # oCell.getPosition()[0]-forceX*debugForceKoeff,
                                 # oCell.getPosition()[1]-forceY*debugForceKoeff,
                                 # arcade.color.BLACK, 0.5)
            #growth
            cell.develop()
            #reproduce
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
    arcade.schedule(on_draw, 1/80)

    # Run the program
    arcade.run()


if __name__ == "__main__":
    main()
