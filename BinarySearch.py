# binary search algorithm

from LinearSearch import LinearSearch

COMPARE = 0
RECURSE = 1
FINISHED = 2

class BinarySearch(LinearSearch):
    def __init__(self, array, mediator):
        super().__init__(array, mediator)
        self.start = 0
        self.end = len(self.array) - 1
        self.mid = self.start + (self.end - self.start) // 2

    def next(self):
        if self.stage == COMPARE:
            # highlight the mid value being compared
            self.mediator.highlight([self.mid])
            # update the description message box
            message = ""
            if self.array[self.mid] == self.item:
                message = "A[mid] = " + str(self.item)
                self.stage = FINISHED
            elif self.array[self.mid] > self.item:
                message = "A[mid] > " + str(self.item)
                # update the stage
                if self.mid - self.start == 0:
                    self.stage = FINISHED
                else:
                    self.stage = RECURSE
            else:
                message = "A[mid] < " + str(self.item)
                # update the stage
                if self.end - self.mid == 0:
                    self.stage = FINISHED
                else:
                    self.stage = RECURSE
            self.mediator.display_description(message)
        elif self.stage == RECURSE:
            self.mediator.highlight([self.mid])
            message = ""
            if self.array[self.mid] > self.item:
                message = "repeat on the left"
                self.end = self.mid - 1
            else:
                message = "repeat on the right"
                self.start = self.mid + 1
            self.mediator.display_description(message)
            self.mediator.shadow(self.start, self.end)
            self.mid = self.start + (self.end - self.start) // 2
            self.stage = COMPARE
        elif self.stage == FINISHED:
            message = ""
            if self.array[self.mid] == self.item:
                message = "result = " + str(self.mid)
            else:
                self.mediator.highlight([-1])
                self.mediator.shadow(-1,-1)
                message = "result = -1"
            self.mediator.display_result(message)
            self.mediator.display_description("")
            self.finished = True
        else:
            raise ValueError

    def get_state(self):
        return (self.start, self.end, self.mid, self.stage, self.finished)

    def set_state(self, state):
        self.start = state[0]
        self.end = state[1]
        self.mid = state[2]
        self.stage = state[3]
        self.finished = state[4]

    def is_started(self):
        if self.stage == COMPARE and self.start == 0 and self.end == len(self.array) - 1:
            return False
        else:
            return True
