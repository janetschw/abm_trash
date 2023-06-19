# from mesa.time import RandomActivation
# from mesa.space import MultiGrid 
# from person import PersonAgent
import numpy as np
import random

class Citizen:
    def __init__(self, x, y, littering_prob):
        self.x = x
        self.y = y
        self.littering_prob = littering_prob

    def move(self, max_x, max_y):
        self.x = random.randrange(0, max_x)
        self.y = random.randrange(0, max_y)

    def throw_trash(self, trash_bins, littering_spots, max_y, max_x):
        if random.random() < self.littering_prob:
            x = random.randrange(0, max_x)
            y = random.randrange(0, max_y)

            if (x, y) not in littering_spots:
                littering_spots.append((x, y))
        else:
            x, y = random.choice(trash_bins)
        return x, y

class ABM:
    def __init__(self, num_citizens, littering_prob, num_steps):
        self.max_x = 10  # maximum x-coordinate of the environment
        self.max_y = 10  # maximum y-coordinate of the environment
        self.trash_bins = [(1, 1), (8, 8), (3, 7)]  # coordinates of trash bins
        self.littering_spots = [(2, 5), (6, 3), (4, 9)]  # coordinates of littering spots
        self.num_steps = num_steps
        self.citizens = []

        for i in range(num_citizens):
            new_citizen = Citizen(
                x=random.randrange(0, self.max_x),
                y=random.randrange(0, self.max_y),
                littering_prob=littering_prob
            )
            self.citizens.append(new_citizen)

    def step(self):
        for citizen in self.citizens:
            citizen.move(self.max_x, self.max_y)
            x, y = citizen.throw_trash(self.trash_bins, self.littering_spots, self.max_x, self.max_y)
            if (x, y) in self.trash_bins:
                print("Citizen threw trash in a trash bin at coordinates:", (x, y))
            else:
                print("Citizen threw trash on the ground at coordinates:", (x, y))

    def run(self):
        for step in range(self.num_steps):
            print("Step", step + 1)
            self.step()
        print("Game over")
        print(self.littering_spots)

# Example usage
num_citizens = 5
littering_prob = 0.2
num_steps = 10

model = ABM(num_citizens, littering_prob, num_steps)
model.run()