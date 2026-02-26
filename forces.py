from CONSTANTS import *

class Speed:
    def __init__(self):
        self.v = 1
    
    def get_v(self):
        return self.v
    
    def set_v(self, v):
        self.v = v

    def update(self):
        if self.v < JUMPFORCE:
            self.v += GRAVITY
        if self.v > JUMPFORCE:
            self.v = JUMPFORCE