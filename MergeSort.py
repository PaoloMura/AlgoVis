# Merge Sort Algorithm

from Algorithm import Algorithm
from Merge import Merge
from Mediator import *
from Tree import *
import math

SPLIT = 0
DOWN = 1
SORTEDSUB = 2
MERGE = 3
UP = 4
FINISHED = 5


class MergeSort(Algorithm):
    def __init__(self, array, mediator:MergeMediator):
        # initialise attributes
        self.tree = Tree(list(array))
        self.mediator = mediator
        self.stage = SPLIT
        self.finished = False
        self.handler = Merge(mediator)
        # setup
        self.mediator.display_result("")
        self.mediator.change_array(CHILD1, [])
        self.mediator.change_array(CHILD2, [])

    def split(self):
        self.mediator.display_description("Split into subarrays")
        array = self.tree.get_value()
        mid = math.ceil(len(array) / 2)
        self.tree.add_children(array[:mid], array[mid:])
        self.mediator.change_array(CHILD1, array[:mid])
        self.mediator.shadow(CHILD1, 0, len(self.tree.get_left()) - 1)
        self.mediator.change_array(CHILD2, array[mid:])
        self.mediator.shadow(CHILD2, 0, len(self.tree.get_right()) - 1)
        self.stage = DOWN

    def go_down(self):
        # decide which branch to follow
        self.tree.go_left()
        if self.tree.is_sorted():
            self.tree.go_up()
            self.tree.go_right()
            self.mediator.display_description("Recurse on the right")
        else:
            self.mediator.display_description("Recurse on the left")
        # update the arrays
        self.mediator.change_array(PARENT, self.tree.get_value())
        self.mediator.shadow(PARENT, 0, len(self.tree.get_value()) - 1)
        self.mediator.change_array(CHILD1, [])
        self.mediator.change_array(CHILD2, [])
        # decide which stage to move onto
        if len(self.tree.get_value()) == 1:
            self.stage = SORTEDSUB
        else:
            self.stage = SPLIT

    def finish_sub(self):
        self.mediator.display_description("The subarray is sorted!")
        self.tree.set_sorted(True)
        self.mediator.shadow(PARENT, 1, 1)
        self.stage = UP

    def merge(self):
        if not self.handler.is_started():
            self.handler.reset(self.tree.get_left(), self.tree.get_right())
            self.handler.next()
        elif self.handler.is_finished():
            self.mediator.display_result("")
            self.mediator.highlight(CHILD1, [])
            self.mediator.highlight(CHILD2, [])
            self.tree.set_value(self.handler.get_parent_array())
            self.tree.set_sorted(True)
            self.tree.remove_children()
            self.handler.reset([], [])
            self.go_up()
        else:
            self.handler.next()

    def go_up(self):
        if self.tree.is_root():
            self.mediator.display_description("")
            self.mediator.change_array(CHILD1, [])
            self.mediator.change_array(CHILD2, [])
            self.stage = FINISHED
        else:
            self.mediator.display_description("Return result to previous layer")
            sorted_children = True
            # set the parent node
            self.tree.go_up()
            current = self.tree.get_value()
            self.mediator.change_array(PARENT, current)
            self.mediator.shadow(PARENT, 0, len(current) - 1)
            # set the left child node
            self.tree.go_left()
            left = self.tree.get_value()
            self.mediator.change_array(CHILD1, left)
            if not self.tree.is_sorted():
                sorted_children = False
                self.mediator.shadow(CHILD1, 0, len(left) - 1)
            else:
                self.mediator.shadow(CHILD1, len(left), len(left))
            self.tree.go_up()
            # set the right child node
            self.tree.go_right()
            right = self.tree.get_value()
            self.mediator.change_array(CHILD2, right)
            if not self.tree.is_sorted():
                sorted_children = False
                self.mediator.shadow(CHILD2, 0, len(right) - 1)
            else:
                self.mediator.shadow(CHILD2, len(right), len(right))
            self.tree.go_up()
            # decide which stage to move on to
            if sorted_children:
                self.stage = MERGE
            else:
                self.stage = DOWN

    def finish(self):
        self.mediator.display_description("")
        self.mediator.display_result("Sorted!")
        self.finished = True

    def next(self):
        if self.stage == SPLIT:
            self.split()
        elif self.stage == DOWN:
            self.go_down()
        elif self.stage == SORTEDSUB:
            self.finish_sub()
        elif self.stage == MERGE:
            self.merge()
        elif self.stage == UP:
            self.go_up()
        elif self.stage == FINISHED:
            self.finish()
        else:
            raise ValueError

    def get_state(self):
        return ([tuple(self.tree.get_state()), self.stage, self.finished, tuple(self.handler.get_state())])

    def set_state(self, state):
        self.tree.set_state(state[0])
        self.stage = state[1]
        self.finished = state[2]
        self.handler.set_state(state[3])

    def is_finished(self):
        return self.finished

    def is_started(self):
        if self.stage == SPLIT and self.tree.is_root():
            return False
        else:
            return True
