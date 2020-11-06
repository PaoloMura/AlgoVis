# Mediator for forwarding requests to the required object

from Array import *

PARENT = 0
CHILD1 = 1
CHILD2 = 2

class Mediator:
    def __init__(self, array:Array, description:MessageBox, result:MessageBox):
        self.array = array
        self.description = description
        self.result = result

    def highlight(self, indices):
        self.array.highlight(indices)
        self.array.update_colours()

    def shadow(self, start, end):
        self.array.shadow(start, end)
        self.array.update_colours()

    def update_values(self, values):
        self.array.update_values(values)

    def change_array(self, values):
        self.array.replace_values(values)

    def display_description(self, message):
        self.description.set_value(message)

    def display_result(self, message):
        self.result.set_value(message)





class MergeMediator:
    def __init__(self, parent_array, child1_array, child2_array, description, result):
        parent_mediator = Mediator(parent_array, description, result)
        child1_mediator = Mediator(child1_array, description, result)
        child2_mediator = Mediator(child2_array, description, result)
        self.mediators = [parent_mediator, child1_mediator, child2_mediator]
        self.description = description
        self.result = result
    
    def highlight(self, node, indices):
        self.mediators[node].highlight(indices)

    def shadow(self, node, start, end):
        self.mediators[node].shadow(start, end)

    def update_values(self, node, values):
        self.mediators[node].update_values(values)

    def change_array(self, node, values):
        self.mediators[node].change_array(values)

    def display_description(self, message):
        self.description.set_value(message)

    def display_result(self, message):
        self.result.set_value(message)
