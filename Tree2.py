import math

import numpy

C = 0.2


class Tree2:

    def __init__(self, n_init=0, v_init=0, depth=0, observation=False):
        self.state_counter = n_init
        self.state_value = v_init  # state value
        self.depth = depth
        self.observation = observation

        self.real_actions = []  # action to take
        self.actions = []  # sub trees

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
        next_state.incement_state_value(r)

    def increment_state_value(self, value):
        self.state_value += (value - self.state_value) / self.state_counter

    def get_state_value(self):
        return self.state_value

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)

    def add_child(self, action):
        self.real_actions.append(action)
        self.actions.append(Tree2(observation=True))

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
            Q_value = node.get_state_value + C * math.sqrt(
                numpy.log(self.get_state_counter()) / node.get_state_counter())
            values.append(Q_value)
        return values

    def is_observation_node(self):
        return self.observation

    def printTree(self):
        if (not self.actions):
            print("empty root")
            return None
        q = []
        print('Root')
        for action in self.actions:
            q.append(action)
        #q.append(root)
        while (len(q) != 0):
            n = len(q)
            numb = 0
            while (n > 0):
                p = q[0]
                q.pop(0)
                #print(p)
                if not p.is_observation_node():
                    print("O"+str(numb), end=" ")
                    for i in range(len(p.actions)):
                        q.append(p.actions[i])
                else:
                    print("a"+str(numb), end=" ")
                    for i in range(len(p.actions)):
                        q.append(p.actions[i])
                n -= 1
                numb += 1
            print()


if __name__ == "__main__":
    ACTION = ['left', 'down', 'right', 'up']
    t = Tree2()
    for action in ACTION:
        t.add_child(action)
    t.actions[0].add_observation(2)
    t.actions[0].add_observation(3)
    t.actions[1].add_observation(2)
    t.printTree(t)
