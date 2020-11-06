# Bubble Sort Algorithm

from Algorithm import Algorithm
from Mediator import Mediator

COMPARE = 0
SWAP = 1
INCREMENT = 2
FINISHED = 3

class BubbleSort(Algorithm):
    def __init__(self, array, mediator:Mediator):
        self.array = list(array)
        self.mediator = mediator
        self.stage = COMPARE
        self.count = 0
        self.end = len(self.array) - 1
        self.finished = False
        self.mediator.display_result("")

    def swap(self):
        temp = self.array[self.count]
        self.array[self.count] = self.array[self.count + 1]
        self.array[self.count + 1] = temp

    def next(self):
        if self.stage == COMPARE:
            self.mediator.highlight([self.count, self.count + 1])
            message = ""
            if self.array[self.count] <= self.array[self.count + 1]:
                message = "A[{}] <= A[{}]"
                self.stage = INCREMENT
            else:
                message = "A[{}] > A[{}]"
                self.stage = SWAP
            message = message.format(str(self.count), str(self.count + 1))
            self.mediator.display_description(message)
        elif self.stage == SWAP:
            self.swap()
            message = "Swap A[{}] and A[{}]".format(str(self.count), str(self.count + 1))
            self.mediator.display_description(message)
            self.mediator.update_values(self.array)
            self.stage = INCREMENT
        elif self.stage == INCREMENT:
            if self.count + 1 == self.end:
                self.mediator.highlight([self.count, self.count + 1])
                # the array is sorted
                if self.count == 0:
                    self.mediator.display_description("A[0] and A[1] are now sorted")
                    self.count = -1
                    self.end = -1
                    self.stage = FINISHED
                # the array may not yet be sorted
                else:
                    message = "A[{}] is now sorted".format(str(self.count + 1))
                    self.mediator.display_description(message)
                    self.count = 0
                    self.end -= 1
                    self.stage = COMPARE
                self.mediator.shadow(self.count, self.end)
            else:
                self.mediator.display_description("increment index")
                self.count += 1
                self.stage = COMPARE
        elif self.stage == FINISHED:
            self.mediator.shadow(-1, -1)
            self.mediator.highlight([])
            self.mediator.display_description("")
            self.mediator.display_result("Sorted!")
            self.finished = True
        else:
            raise ValueError

    def get_state(self):
        return (self.stage, self.count, self.end, self.finished, tuple(self.array))

    def set_state(self, state):
        self.stage = state[0]
        self.count = state[1]
        self.end = state[2]
        self.finished = state[3]
        self.array = list(state[4])

    def is_finished(self):
        return self.finished

    def is_started(self):
        if self.stage == COMPARE and self.count == 0 and self.end == len(self.array) - 1:
            return False
        else:
            return True
