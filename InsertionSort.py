# Insertion Sort Algorithm

from Algorithm import Algorithm
from Mediator import Mediator

COMPARE = 0
SWAP = 1
INCREMENT = 2
FINISHED = 3

class InsertionSort(Algorithm):
    def __init__(self, array, mediator:Mediator):
        self.array = list(array)
        self.mediator = mediator
        self.stage = COMPARE
        self.i = 1  # the outer loop pointer
        self.j = 1  # the inner loop pointer
        self.end = len(self.array) - 1
        self.finished = False
        self.mediator.display_result("")
        self.mediator.shadow(2, self.end)
        self.mediator.highlight([1])

    def swap(self):
        temp = self.array[self.j]
        self.array[self.j] = self.array[self.j - 1]
        self.array[self.j - 1] = temp

    def next(self):
        if self.stage == COMPARE:
            message = ""
            if self.array[self.j] < self.array[self.j - 1]:
                message = "A[{}] < A[{}]"
                self.stage = SWAP
            else:
                message = "All values left of A[i] are sorted"
                self.stage = INCREMENT
            message = message.format(str(self.j), str(self.j - 1))
            self.mediator.display_description(message)
        elif self.stage == SWAP:
            self.swap()
            message = "Swap A[{}] and A[{}]".format(str(self.j), str(self.j - 1))
            self.mediator.display_description(message)
            self.mediator.update_values(self.array)
            self.j -= 1
            self.mediator.highlight([self.j])
            if self.j == 0:
                self.stage = INCREMENT
            else:
                self.stage = COMPARE
        elif self.stage == INCREMENT:
            self.mediator.display_description("Increment i")
            if self.i == self.end:
                self.stage = FINISHED
                self.end += 1
            else:
                self.stage = COMPARE
            self.i += 1
            self.j = self.i
            self.mediator.shadow(self.i+1, self.end)
            self.mediator.highlight([self.j])
        elif self.stage == FINISHED:
            self.mediator.display_description("")
            self.mediator.display_result("Sorted!")
            self.finished = True
        else:
            raise ValueError

    def get_state(self):
        return (self.stage, self.i, self.j, self.end, self.finished, tuple(self.array))

    def set_state(self, state):
        self.stage = state[0]
        self.i = state[1]
        self.j = state[2]
        self.end = state[3]
        self.finished = state[4]
        self.array = list(state[5])

    def is_finished(self):
        return self.finished

    def is_started(self):
        if self.stage == COMPARE and self.i == 1 and self.j == 1:
            return False
        else:
            return True
