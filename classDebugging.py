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

import math
import pprint

class Test:
    var = 0
    def __init__(self, var, mass):
        self.var = var
        self.physics = {
                "velocity":[0,0],
                "mass":mass,
                "position":[0,0],
                "charge":0,
                }

    def printVars(self):
        print("var: ", self.var)
        print("mass: ", self.physics["mass"])

class Cell:
    timeCounter = {
            'after_birth':0,
            'after_child': 0
            }
    parent = None
    bio_state = {
                'isRoot': False, # ∞ mass
                'hasChildren': False,
                'size': 0,  # for both stems and berries
                'width': 0, # for both stems and berries
                'type':'stem',
                'color':'#FFFFFF'
            }
    dna = {
            "space_required_for_reproduction": 20,
            "time_before_reproduction": 20,
            } #TODO
    physics = {
            "velocity":[0,0],
            "mass":1.0,
            "position":[0,0],
            "charge":0,
            }

    def __init__(self, position=[100,100], mass=1, parent=None):
        self.physics["position"] = position
        self.physics["mass"] = mass
        self.parent = parent
        # import pdb;pdb.set_trace() 

    def isReproductable(self):
        return self.timeCounter["after_birth"] > self.dna["time_before_reproduction"]

    def applyForce(self, force):
        # print(self.physics["mass"])
        # root doesn't move:
        if self.parent:
            self.physics["velocity"][0] += force[0] / self.physics["mass"]
            self.physics["velocity"][1] += force[1] / self.physics["mass"]
            self.physics["position"][0] += self.physics["velocity"][0]
            self.physics["position"][1] += self.physics["velocity"][1]
        else:
            self.physics["position"][0] = 60
            self.physics["position"][1] = 60

    def reproduce(self):
        return [Cell(position=self.physics["position"], parent=self)]

    def getPosition(self):
        return self.physics["position"]


class Scene:
    cells = []
    # Потом доделать Параметры вьюпорта (проекция координат мира на экран)

    def __init__(self):
        cell2 = Cell()
        cell1 = Cell()
        cell2.physics['mass'] = 1
        pprint.pprint(cell1.physics['mass'])
        pprint.pprint(cell2.physics['mass'])
        pprint.pprint(Cell)
        self.cells.append(cell1)
        self.cells.append(cell2)

    def render(self):
        for cell in self.cells:
            if cell.parent:
                beginPoint = cell.getPosition()
                endPoint = cell.parent.getPosition()
                #print (beginPoint, endPoint)

    def develop(self):
        for cell in self.cells:
            #physics
            cell.applyForce((0,0.01))
            #growth
            cell.size = math.log10(cell.timeCounter["after_birth"] + 2)
            #reproduce
            # if cell.isReproductable():
                # self.cells.extend(cell.reproduce())
            #increasing timer
            cell.timeCounter["after_birth"] += 1


    def coordsWorldToScreen(self):
        return 1;


def main():
    # scene = Scene()
    # scene.render()
    # scene.develop()
    t1 = Test(1, 10)
    t2 = Test(2, 20)
    print("test 1 and 2")
    t1.printVars()
    t2.printVars()


    
    print("cells 1 and 2")
    cell1 = Cell()
    cell2 = Cell()
    cell1.physics['mass'] = 1
    cell2.physics['mass'] = 2
    pprint.pprint(cell1.physics['mass'])
    pprint.pprint(cell2.physics['mass'])


if __name__ == "__main__":
    main()
