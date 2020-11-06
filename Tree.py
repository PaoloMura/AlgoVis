# recursion tree for merge sort

# a node in the tree
class Node:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
        self.sorted = False
        self.left = None
        self.right = None

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_parent(self):
        return self.parent

    def set_left(self, subtree):
        self.left = subtree

    def set_right(self, subtree):
        self.right = subtree

    def get_value(self):
        return list(self.value)

    def set_value(self, value):
        self.value = tuple(value)

    def is_sorted(self):
        return self.sorted

    def set_sorted(self, value):
        self.sorted = value




# binary tree of nodes
class Tree:
    def __init__(self, value):
        self.root = Node(value, None)
        self.current = self.root

    # adds 2 children to the current node
    def add_children(self, value1, value2):
        self.current.set_left(Node(value1, self.current))
        self.current.set_right(Node(value2, self.current))

    # removes the current node's children
    def remove_children(self):
        self.current.set_left(None)
        self.current.set_right(None)

    # captures the state of the given node in the tree
    def get_snapshot(self, node, state):
        # create a snapshot for the given node
        has_children = True
        if node.get_left() == None:
            has_children = False
        is_current = False
        if self.current == node:
            is_current = True
        snapshot = (tuple(node.get_value()), node.is_sorted(), has_children, is_current)
        state.append(snapshot)
        # recursively create snapshots for its children to build up the state
        if has_children:
            self.get_snapshot(node.get_left(), state)
            self.get_snapshot(node.get_right(), state)

    # captures the tree's state as a tuple of snapshots (where each snapshot is a tuple for a node's state)
    def get_state(self):
        state = []
        self.get_snapshot(self.root, state)
        return state

    def restore_snapshot(self, state:tuple, current_snapshot, parent):
        # extract the values
        i = current_snapshot[0]
        value = list(state[i][0])
        is_sorted = state[i][1]
        has_children = state[i][2]
        is_current = state[i][3]
        # reconstruct the node
        node = Node(value, parent[len(parent)-1])
        if is_sorted:
            node.set_sorted(True)
        if is_current:
            self.current = node
        current_snapshot[0] +=1
        # reconstruct its children
        if has_children:
            parent.append(node)
            left = self.restore_snapshot(state, current_snapshot, parent)
            right = self.restore_snapshot(state, current_snapshot, parent)
            node.set_left(left)
            node.set_right(right)
            parent.pop(len(parent)-1)
        return node

    # restores the tree's state according to the given tuple of snapshots (see above)
    def set_state(self, state:tuple):
        parent = [None]
        current_snapshot = [0]
        self.root = self.restore_snapshot(state, current_snapshot, parent)

    def get_value(self):
        if self.current == None:
            return None
        else:
            return self.current.get_value()

    def set_value(self, value):
        self.current.set_value(value)

    def get_left(self):
        if self.current.get_left() == None:
            return []
        else:
            return self.current.get_left().get_value()

    def get_right(self):
        if self.current.get_right() == None:
            return []
        else:
            return self.current.get_right().get_value()
    
    def is_sorted(self):
        return self.current.is_sorted()

    def set_sorted(self, value):
        self.current.set_sorted(value)
    
    def is_root(self):
        if self.current == self.root:
            return True
        else:
            return False

    def go_left(self):
        if self.current.get_left() != None:
            self.current = self.current.get_left()

    def go_right(self):
        if self.current.get_right() != None:
            self.current = self.current.get_right()

    def go_up(self):
        self.current = self.current.get_parent()

    # for testing purposes:
    def view_layer(self, node, depth):
        if depth == 1:
            return str(node.get_value())
        else:
            if node.get_left() == None:
                return ""
            else:
                left = self.view_layer(node.get_left(), depth - 1)
                right = self.view_layer(node.get_right(), depth - 1)
                if left == "" and right == "":
                    return ""
                else:
                    return left + "\t" + right

    # for testing purposes:
    def view_tree(self):
        depth = 1
        node = self.root
        bottom = False
        while not bottom:
            layer = self.view_layer(node, depth)
            if layer == "":
                bottom = True
            else:
                print(layer)
                depth += 1
