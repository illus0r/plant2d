# nmap <D-5> diw"_s["pa"]
# imap <D-5> <ESC>diw"_s["pa"]a

# import arcade
import math
import pprint
import random
from tkinter import *
from PIL import Image, ImageDraw

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

class DNA:
    def __init__(self):
        self.types = [ # indexes refer to self.bioState["type"]
            { #type 0
                "angle": 60, # -180<=angle<=180
                "sizeMultiplier": 0.95,
                "branchSegments": 30,
                "color": 'red',
                "slots": [
                    # {
                        # "type": 0,
                        # "angle": 10,
                        # "sizeMultiplier": 0.5,
                        # },
                    # {
                        # "type": 1,
                        # "angle": -45,
                        # "sizeMultiplier": 0.5,
                        # },
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
    cells = []
    def __init__(self, dna, tk):
        self.canvas = Canvas(tk, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.canvas.pack()
        self.cells.extend(
                    [Cell(size=40, dna=dna, position=[SCREEN_WIDTH/2, SCREEN_HEIGHT/2])]
                )

    def render(self):
        self.canvas.delete("all")
        [c.render(self.canvas) for c in self.cells]

    def develop(self):
        for c in self.cells:
            c.children=[]
            # print(c.dna.types[0]["branchSegments"])
            c.develop()

    def coordsWorldToScreen(self):
        return 1;

    def printDNA(self):
        [c.printDNA() for c in self.cells]


class Controller:
    def __init__(self):
        self.tk = Tk()
        self.dna = DNA()
        self.scene = Scene(self.dna, self.tk)
        #
        # angleWidget = Scale(self.tk, from_=-180, to=180, orient=HORIZONTAL)
        self.angleVar = StringVar()
        self.angleVar.set(5)
        # self.angleVar.trace("u", self.update)
        angleWidget = Entry(self.tk, textvariable=self.angleVar)
        angleWidget.pack()
        angleWidget.bind("<Button-1>", self.update)

        # self.myvar = StringVar()
        # self.myvar.set('')
        # self.mywidget = Entry(self.tk,textvariable=self.myvar,width=100)
        # self.mywidget.pack()
        # self.myvar.trace('u',self.oddblue)
    # def oddblue(self,a,b,c):
        # if len(self.self.myvar.get())%2 == 0:
            # self.mywidget.config(bg='red')
        # else:
            # self.mywidget.config(bg='blue')
        # self.mywidget.update_idletasks()

        # def callback(event):
            # print("clicked at", event.x, event.y)
        # canvas.bind("<B1-Motion>", callback)
        # w.bind("<Button-1>", self.update)
        mainloop()

    def update(self, event):
        # update dna
        self.dna.types[1]["branchSegments"] = int(self.angleVar.get())
        self.scene.cells[0].dna.types[1]["branchSegments"] = int(self.angleVar.get())
        self.dna.types[0]["branchSegments"] = int(self.angleVar.get())
        self.scene.cells[0].dna.types[0]["branchSegments"] = int(self.angleVar.get())
        # self.dna.types[self.bioState["type"]]["branchSegments"]

        # recalc & render
        # del self.scene
        # self.scene = Scene(self.dna, self.tk)
        self.scene.develop(self.dna)
        self.scene.render()
        # self.scene.printDNA()


class Cell:
    parent = None

    def __init__(self, position=[300,300], mass=1, parent=None, level=0, levelBranch=0, angle=0, size=50, type_=0, color='red', dna=DNA()):
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
                # 'width': 0, # for both stems and berries
                'type': type_,
                'color': color,
                'level': level,
                'levelBranch': levelBranch,
                'angle': angle,
                # 'deltaAngle': 0,
                # 'angleVariance': 90,
            }
        self.physics = {
                "position": position,
                }
        self.parent = parent

    # def is(self):
        # if not self.parent:
            # return self.timeCounter["after_birth"] == 0
        # return self.timeCounter["after_birth"] == self.dna.time_before_reproduction

    def applyForce(self, force):
        # root doesn't move:
        # if self.parent:
        # self.physics["velocity"][0] += force[0] / self.physics["mass"]
        # self.physics["velocity"][1] += force[1] / self.physics["mass"]
        pass

    def develop(self):
        # move
        if self.parent:
            vector = [self.bioState["size"] * f(math.radians(self.bioState["angle"])) for f in [math.sin, math.cos] ]
            self.physics["position"] = [b+v for b, v in zip(self.parent.physics["position"], vector)]
        #reproduce
        self.reproduce()
        # recursive developing children
        [c.develop() for c in self.children]


    def reproduce(self):
        # print(self.dna.types[self.bioState["type"]]["branchSegments"])
        if self.bioState["level"] == 0:
            self.children.extend([Cell(
                size=40, 
                level=1,
                levelBranch=1,
                angle=a, 
                type_=0 
            ) for a in range(0,360,30)])

        elif self.bioState["level"] <= 70:
            if self.bioState["levelBranch"] <= self.dna.types[self.bioState["type"]]["branchSegments"]:
                self.children.extend([Cell(
                        parent=self,
                        angle=self.bioState["angle"] + self.dna.types[self.bioState["type"]]["angle"],
                        level=self.bioState["level"]+1,
                        levelBranch=self.bioState["levelBranch"]+1,
                        # color = self.bioState["color"],
                        type_ = self.bioState["type"],
                        size=self.bioState["size"]*self.dna.types[self.bioState["type"]]["sizeMultiplier"],
                    )])
            else:
                self.children.extend([Cell(
                        parent=self,
                        angle=self.bioState["angle"] + slot["angle"],
                        level=self.bioState["level"] + 1,
                        levelBranch=0,
                        # color = ,
                        type_=slot["type"],
                        size=self.bioState["size"] * slot["sizeMultiplier"],
                    ) for slot in self.dna.types[self.bioState["type"]]["slots"]])


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
                # ), fill=self.bioState["color"], 
                fill=self.dna.types[self.bioState["type"]]["color"],                        
                width=int(0.5*math.log(self.bioState["size"]))
                )
        [c.render(canvas) for c in self.children]

    # def getPosition(self):
        # return self.physics["position"]

    def getCharge(self):
        return self.physics["charge"]

    def printDNA(self):
        print(self.dna.types[self.bioState["type"]]["branchSegments"])




# def on_draw(delta_time):
    # arcade.start_render()
    # scene.develop()
    # scene.render()
    # arcade.draw_line(10,10,200,200,            arcade.color.RED,             1)

def main():

    # # Example with update
    # root = Tk()
    # myvar = StringVar()
    # myvar.set('')
    # mywidget = Entry(root,textvariable=myvar,width=10)
    # mywidget.pack()
    # def oddblue(a,b,c):
        # if len(myvar.get())%2 == 0:
            # mywidget.config(bg='red')
        # else:
            # mywidget.config(bg='blue')
        # mywidget.update_idletasks()
    # myvar.trace('u',oddblue)
    # root.mainloop()

    controller = Controller()




if __name__ == "__main__":
    main()
