# States, using Memento Pattern


# a snapshot of the state of the program
class Memento:
    def __init__(self, array_state, description_state, result_state, algo_state):
        self.array_state = tuple(array_state)
        self.description_state = description_state
        self.result_state = result_state
        self.algo_state = tuple(algo_state)

class MergeMemento(Memento):
    def __init__(self, parent_state, child1_state, child2_state, description_state, result_state, algo_state):
        super().__init__(parent_state, description_state, result_state, algo_state)
        self.child1_state = tuple(child1_state)
        self.child2_state = tuple(child2_state)


# stack of mementos
class MementoStack:
    def __init__(self):
        self.mementos = []

    def push_memento(self, memento):
        self.mementos.append(memento)

    def pop_memento(self):
        last = len(self.mementos) - 1
        if last >= 0:
            return self.mementos.pop(len(self.mementos)-1)
        else:
            return None

    # for testing purposes
    def view_stack(self):
        for m in self.mementos:
            print("parent:", m.array_state)
            if type(m) == MergeMemento:
                print("child1:", m.child1_state)
                print("child2:", m.child2_state)
            print("description:", m.description_state)
            print("result:", m.result_state)
            print("algorithm:", m.algo_state)
            print("tree:", m.algo_state[0])
            print("\n")
