# Merge Algorithm


from Algorithm import Algorithm
from Mediator import *
from Tree import *

DORMANT = 0
COMPARE = 1
INSERT = 2
NEXT = 3
FINISHED = 4


class Merge(Algorithm):
    def __init__(self, mediator:MergeMediator):
        self.mediator = mediator
        self.stage = DORMANT
        self.i = 0  # the pointer for the left child
        self.j = 0  # the pointer for the right child
        self.count = 0  # the pointer for the parent
        self.finished = False
        self.parent = []
        self.left_child = []
        self.right_child = []

    # a secondary constructor
    def reset(self, left_child:list, right_child:list):
        # initialise attributes
        self.parent = [""] * (len(left_child) + len(right_child))
        self.left_child = left_child
        self.right_child = right_child
        self.stage = COMPARE
        self.i = 0
        self.j = 0
        self.count = 0
        self.finished = False
        # setup
        self.mediator.update_values(PARENT, self.parent)
        self.mediator.shadow(PARENT, 0, len(self.parent) - 1)
        self.mediator.display_result("")

    def update_colours(self):
        self.mediator.shadow(CHILD1, self.i, len(self.left_child)-1)
        self.mediator.shadow(CHILD2, self.j, len(self.right_child)-1)
        self.mediator.highlight(CHILD1, [self.i])
        self.mediator.highlight(CHILD2, [self.j])

    def next(self):
        if self.stage == DORMANT:
            pass
        elif self.stage == COMPARE:
            self.update_colours()
            message = ""
            if self.left_child[self.i] <= self.right_child[self.j]:
                message = "A[{}] <= B[{}]"
            else:
                message = "A[{}] > B[{}]"
            self.mediator.display_description(message.format(self.i, self.j))
            self.stage = INSERT
        elif self.stage == INSERT:
            self.update_colours()
            if self.i < len(self.left_child) and self.j < len(self.right_child):
                if self.left_child[self.i] <= self.right_child[self.j]:
                    self.mediator.display_description("Insert A[{}] into the array".format(self.i))
                    self.parent[self.count] = self.left_child[self.i]
                    self.i += 1
                    if self.i == len(self.left_child):
                        self.stage = INSERT
                    else:
                        self.stage = COMPARE
                else:
                    self.mediator.display_description("Insert B[{}] into the array".format(self.j))
                    self.parent[self.count] = self.right_child[self.j]
                    self.j += 1
                    if self.j == len(self.right_child):
                        self.stage = INSERT
                    else:
                        self.stage = COMPARE
            elif self.i < len(self.left_child):
                self.mediator.display_description("Insert A[{}] into the array".format(self.i))
                self.parent[self.count] = self.left_child[self.i]
                self.i += 1
                if self.i == len(self.left_child):
                    self.stage = FINISHED
                else:
                    self.stage = NEXT
            elif self.j < len(self.right_child):
                self.mediator.display_description("Insert B[{}] into the array".format(self.j))
                self.parent[self.count] = self.right_child[self.j]
                self.j += 1
                if self.j == len(self.right_child):
                    self.stage = FINISHED
                else:
                    self.stage = NEXT
            self.mediator.update_values(PARENT, self.parent)
            self.count += 1
            self.mediator.shadow(PARENT, self.count, len(self.parent))
        elif self.stage == NEXT:
            if self.i < len(self.left_child):
                self.mediator.display_description("Increment i")
                self.mediator.shadow(CHILD1, self.i, len(self.left_child)-1)
                self.mediator.highlight(CHILD1, [self.i])
            else:
                self.mediator.display_description("Increment j")
                self.mediator.shadow(CHILD2, self.j, len(self.right_child)-1)
                self.mediator.highlight(CHILD2, [self.j])
            self.stage = INSERT
        elif self.stage == FINISHED:
            self.mediator.highlight(CHILD1, [])
            self.mediator.highlight(CHILD2, [])
            self.update_colours()
            self.mediator.display_description("")
            self.mediator.display_result("Sorted subarray!")
            self.finished = True
        else:
            raise ValueError

    def get_parent_array(self):
        return self.parent

    def get_state(self):
        return ([tuple(self.parent), tuple(self.left_child), self.i, tuple(self.right_child), self.j, self.count, self.stage, self.finished])

    def set_state(self, state):
        self.parent = list(state[0])
        self.left_child = list(state[1])
        self.i = state[2]
        self.right_child = list(state[3])
        self.j = state[4]
        self.count = state[5]
        self.stage = state[6]
        self.finished = state[7]

    def is_finished(self):
        return self.finished

    def is_started(self):
        if self.stage == DORMANT or self.stage == COMPARE and self.i == 0 and self.j == 0 and self.count == 0:
            return False
        else:
            return True
