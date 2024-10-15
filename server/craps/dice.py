import random

class Dice:
    def __init__(self, sides=6):
        self.sides = sides
        self.value = 1

    def roll(self):
        self.value = random.randint(1, self.sides)
        return self.value

class DicePair:
    def __init__(self):
        self.dice1 = Dice()
        self.dice2 = Dice()

    def roll_sum(self):
        self.roll()
        return self.sum()

    def roll(self):
        return self.dice1.roll(), self.dice2.roll()

    def sum(self):
        return self.dice1.value + self.dice2.value

    def is_hardway(self):
        return self.dice1.value == self.dice2.value and self.sum() in [4, 6, 8, 10]

    def is_craps(self):
        return self.sum() in [2, 3, 12]

    def is_natural(self):
        return self.sum() in [7, 11]