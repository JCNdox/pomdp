import math
import numpy
C = 0.2

class Tree2:

    def __init__(self, n_init=0, v_init=0, depth=0):
        self.state_counter = n_init
        self.state_value = v_init     # state value
        self.depth = depth

        self.real_actions = []  # action to take
        self.actions = []       # sub trees

        self.states = []

    def get_state_counter(self):
        return self.state_counter

    def increment_state_counter(self):
        self.state_counter += 1

    def increment_action_counter(self, action):
        next_state = self.get_leading_state(action)
        next_state.increment_state_counter()

    def increment_next_state_value(self, action, r):
        next_state = self.get_leading_state(action)
        value = r
        next_state.incement_state_value(value)

    def increment_state_value(self, value):
        self.state_value += (value - self.state_value)/self.state_counter

    def get_state_value(self):
        return self.state_value

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)

    def add_child(self, action):
        self.real_actions.append(action)
        self.actions.append(Tree2())

    def add_observation(self, observation):
        self.real_actions.append(observation)
        self.actions.append(Tree2())

    def get_leading_state(self, action):
        pos = 0
        for child in self.real_actions:
            if child == action:
                break
            pos += 1
        return self.actions[pos]

    def contains(self, action):
        return action in self.real_actions

    def next_state_values(self):
        values = []
        for node in self.actions:
            Q_value = node.get_state_value + C * math.sqrt(numpy.log(self.get_state_counter())/node.get_state_counter())
            values.append(node.state_value)
        return values

    def printTree(self, root):
        pass


if __name__ == "__main__":
    t = Tree2()
