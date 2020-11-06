# Linear Search

from Mediator import Mediator
from Algorithm import Algorithm
import random

CHANCE = 0.8

COMPARE = 0
INCREMENT = 1
FINISHED = 2

class LinearSearch(Algorithm):
    def __init__(self, array, mediator:Mediator):
        self.array = array
        self.item = 0
        if random.random() >= (1 - CHANCE):
            self.item = random.choice(array)
        else:
            self.item = random.randint(0,99)
        self.count = 0
        self.finished = False
        self.mediator = mediator
        self.stage = COMPARE

    def next(self):
        if self.stage == COMPARE:
            self.mediator.highlight([self.count])
            if self.array[self.count] == self.item:
                message = "A[" + str(self.count) + "] = " + str(self.item)
                self.mediator.display_description(message)
                self.stage = FINISHED
            else:
                message = "A[" + str(self.count) + "] ≠ " + str(self.item)
                self.mediator.display_description(message)
                self.stage = INCREMENT
        elif self.stage == INCREMENT:
            self.mediator.display_description("increment index")
            self.count += 1
            if self.count == len(self.array):
                self.stage = FINISHED
            else:
                self.stage = COMPARE
        elif self.stage == FINISHED:
            self.mediator.display_description("")
            if self.count == len(self.array):
                self.mediator.highlight([self.count])
                self.mediator.display_result("result = -1")
            else:
                self.mediator.display_result("result = " + str(self.count))
            self.finished = True
        else:
            raise ValueError

    def get_state(self):
        return (self.count, self.finished, self.stage)

    def set_state(self, state):
        self.count = state[0]
        self.finished = state[1]
        self.stage = state[2]

    def get_item(self):
        return self.item

    def is_finished(self):
        return self.finished

    def is_started(self):
        if self.stage == COMPARE and self.count == 0:
            return False
        else:
            return True
