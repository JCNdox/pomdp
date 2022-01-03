

class Tree2:

    def __init__(self, n_init=0, v_init=0, depth=0):
        self.state_counter = n_init
        self.state_value = v_init     # state value
        self.depth = depth

        self.real_actions = []  # action to take
        self.actions = []       # sub trees

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

    def printTree(self, root):
        pass


if __name__ == "__main__":
    t = Tree2()
