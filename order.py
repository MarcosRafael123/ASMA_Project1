import pandas as pd

orders1 = []
orders2 = []

class Order:
    def __init__(self, id=None, pos=(), weight=None):
        self.id = id
        self.pos = pos
        self.weight = weight