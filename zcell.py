class Cell:
    timeCounter = {
            'after_birth':0,
            'after_child': 0
            }
    children = []
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
            "velocity":(0,0),
            "mass":0,
            "position":(0,0),
            "charge":0,
            }

    def __init__(self, position):
        self.physics.position = position
        print(position)

    def isReproductable(self):
        return self.timeCounter.after_birth > self.dna.time_before_reproduction

    def growth(self):
        self.size = math.log10(self.time.after_birth + 2)


