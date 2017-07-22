# nmap <D-5> diw"_s["pa"]
# imap <D-5> <ESC>diw"_s["pa"]a

import math
import pprint
import random
from tkinter import *
from PIL import Image, ImageDraw

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# TODO list:
# 1. Try to import to blender. May be sverchok's interface can replace tkinter

class DNAType:
    def __init__(self, angle=60, sizeMultiplier=1, branchSegments=5, color='green', slots=[]):
        self.angle = angle # -180<=angle<=180
        self.sizeMultiplier = sizeMultiplier
        self.branchSegments = branchSegments
        self.color = color
        self.slots = slots
                    # { # "TYPE": 0, # "ANGLE": 10, # "SIZEMULTIPLIER": 0.5, # }, # { # "TYPE": 1, # "ANGLE": -45, # "SIZEMULTIPLIER": 0.5, # },

class DNA:
    def __init__(self):
        self.initialBranchNumber = 0
        self.types = [ # indexes refer to self.bioState["type"]
            DNAType(
                angle = 60, # -180<=angle<=180
                sizeMultiplier = 0.95,
                branchSegments = 8,
                color = 'red',
                ),
            DNAType(
                angle = 60, # -180<=angle<=180
                sizeMultiplier = 1,
                branchSegments = 5,
                color = 'green',
                slots = [
                    # { # "TYPE": 0, # "ANGLE": 10, # "SIZEMULTIPLIER": 0.5, # }, # { # "TYPE": 1, # "ANGLE": -45, # "SIZEMULTIPLIER": 0.5, # },
                    ]
                ),

            { #type 0
                "angle": 60, # -180<=angle<=180
                "sizeMultiplier": 0.95,
                "branchSegments": 8,
                "color": 'red',
                "slots": [
                    ],
                },
            { #type 1
                "angle": 60, # -180<=angle<=180
                "sizeMultiplier": 1,
                "branchSegments": 5,
                "color": 'green',
                "slots": [
                    ],
                },
            ]


class Scene:
    def __init__(self, tk):
        self.canvas = Canvas(tk, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.canvas.pack()
        pass

    def render(self):
        self.canvas.delete("all")
        [c.render(self.canvas) for c in self.cells]

    def develop(self, dna):
        print("Scene:         ",dna)
        self.cells = []
        self.cells.extend(
                [Cell(size=40, dna=dna, position=[SCREEN_WIDTH/2, SCREEN_HEIGHT/2])]
            )
        for c in self.cells:
            c.children=[]
            c.develop()

    def coordsWorldToScreen(self):
        return 1;

    def printDNA(self):
        [c.printDNA() for c in self.cells]


class Controller:
    def __init__(self):
        self.tk = Tk()
        self.dna = DNA()
        self.scene = Scene(self.tk)
        # initialBranchNumber
        self.dna.initialBranchNumber = IntVar()
        self.dna.initialBranchNumber.set(3)
        self.dna.initialBranchNumber.trace("w", self.update)
        initialBranchNumberWidget = Scale(self.tk, from_=0, to=100, orient=HORIZONTAL, 
                variable=self.dna.initialBranchNumber)
        initialBranchNumberWidget.pack()
        # Angle
        self.dna.types[0].angle = IntVar()
        self.dna.types[0].angle.set(5)
        self.dna.types[0].angle.trace("w", self.update)
        angleWidget = Scale(self.tk, from_=-180, to=180, orient=HORIZONTAL, 
                variable=self.dna.types[0].angle)
        angleWidget.pack()
        # sizeMultiplier
        self.dna.types[0].sizeMultiplier = IntVar()
        self.dna.types[0].sizeMultiplier.set(90)
        self.dna.types[0].sizeMultiplier.trace("w", self.update)
        sizeMultiplierWidget = Scale(self.tk, from_=0, to=100, orient=HORIZONTAL, 
                variable=self.dna.types[0].sizeMultiplier)
        sizeMultiplierWidget.pack()
        #
        self.update()
        mainloop()

    def update(self, *args):
        # update dna
        # self.dna.types[0].angle = int(self.dna.types[0].angle.get())

        # self.scene.cells[0].dna.types[0]["branchSegments"] = int(self.angleVar.get())
        print("Controller:    ",self.dna)

        # recalc & render
        # del self.scene
        # self.scene = Scene(self.dna, self.tk)
        self.scene.develop(self.dna)
        self.scene.render()
        # self.scene.printDNA()


class Cell:
    parent = None

    def __init__(self, position=[300,300], mass=1, parent=None, level=0, levelBranch=0, angle=0, size=50, type_=0, color='red', dna=DNA()):
        print("Cell init:     ",dna, level)
        self.dna = dna
        self.children = []
        self.timeCounter = {
                'after_birth': 0,
                'after_child': 0,
                }
        self.bioState = {
                'isRoot': False, # ∞ mass
                'hasChildren': False,
                'size': size,  # for both stems and berries
                'type': type_,
                'color': color,
                'level': level,
                'levelBranch': levelBranch,
                'angle': angle,
            }
        self.physics = {
                "position": position,
                }
        self.parent = parent


    def develop(self):
        # move
        if self.parent:
            vector = [self.bioState["size"] * f(math.radians(self.bioState["angle"])) for f in [math.sin, math.cos] ]
            self.physics["position"] = [b+v for b, v in zip(self.parent.physics["position"], vector)]
        self.reproduce()
        [c.develop() for c in self.children]


    def reproduce(self):
        # print("Cell reproduce:",self.dna)
        # print(self.dna.types[self.bioState["type"]]["branchSegments"])
        if self.bioState["level"] == 0:
            self.children.extend([Cell(
                size=40, 
                level=1,
                levelBranch=1,
                dna=self.dna,
                angle=a/100, 
                type_=0 
            ) for a in range(0,35900,int(36000/self.dna.initialBranchNumber.get()))])

        elif self.bioState["level"] <= 70:
            if self.bioState["levelBranch"] <= self.dna.types[self.bioState["type"]].branchSegments:
                self.children.extend([Cell(
                        parent=self,
                        angle=self.bioState["angle"] + self.dna.types[self.bioState["type"]].angle.get(),
                        level=self.bioState["level"]+1,
                        levelBranch=self.bioState["levelBranch"]+1,
                        type_ = self.bioState["type"],
                        dna=self.dna,
                        size=self.bioState["size"]*self.dna.types[self.bioState["type"]].sizeMultiplier.get()/100,
                    )])
            else:
                self.children.extend([Cell(
                        parent=self,
                        angle=self.bioState["angle"] + slot["angle"],
                        level=self.bioState["level"] + 1,
                        levelBranch=0,
                        type_=slot["type"],
                        dna=self.dna,
                        size=self.bioState["size"] * slot["sizeMultiplier"],
                    ) for slot in self.dna.types[self.bioState["type"]].slots])


    def render(self, canvas):
        if self.parent:
            beginPoint = self.parent.physics["position"]
            endPoint = self.physics["position"]
            # canvas.ellipse((
                # beginPoint[0]-1, beginPoint[1]-1, 
                # beginPoint[0]+1, beginPoint[1]+1, 
                # ), 
                # fill = 'red')
            canvas.create_line(
                beginPoint[0], beginPoint[1], 
                endPoint[0], endPoint[1], 
                fill=self.dna.types[self.bioState["type"]].color,                        
                width=int(0.5*math.log(self.bioState["size"]))
                )
        [c.render(canvas) for c in self.children]

    def getCharge(self):
        return self.physics["charge"]

    def printDNA(self):
        print(self.dna.types[self.bioState["type"]]["branchSegments"])


def main():
    controller = Controller()

if __name__ == "__main__":
    main()
