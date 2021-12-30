ACTION = ['left', 'down', 'right', 'up']


class Tree:

    def __init__(self, number_of_actions, n_init=0, v_init=0, depth=0, decision_state=False):
        self.number_of_actions = number_of_actions
        self.state_counter = n_init
        self.state_value = v_init     # state value
        self.depth = depth

        if decision_state:
            self.actions = []      # state's actions
            self.actions_counter = []   # actions counter
            self.belief_state = None    # state's belief state
            self.insert()
        else:
            self.observations = []      # state's observations
            self.leading_state = []     # observation leads you to next_state

    def getDepth(self):
        return self.depth

    def getChildren(self):
        return self.actions

    def insert_observation(self, observation):
        self.observations.append(observation)
        self.leading_state.append(Tree(depth=self.depth + 1, decision_state=True))

    def get_observation_pos(self, observation):
        if observation in self.observations:
            for j in range(len(self.observations)):
                if self.observations[j] == observation:
                    return j
        return None

    def insert(self):
        for action in range(self.number_of_actions):
            self.actions.append(Tree(depth=self.depth + 1))

    def next_state_values(self):
        values = []
        for node in self.actions:
            values.append(node.state_value)
        return values

    def printTree(self):
        print("S0")
        for i in range(len(t.getChildren())):
            print("a" + str(i), end=" ")
        print()
        for i in range(len(t.getChildren())):
            for j in range(len(t.actions[i].observations)):
                print(t.actions[i].observations[j], end=" ")
        print()
        for i in range(len(t.getChildren())):
            for j in range(len(t.actions[i].observations)):
                for h in range(len(t.actions[i].leading_state)):
                    for e in range(len(t.actions[i].leading_state[h].getChildren())):
                        print("a" + str(e), end=" ")


if __name__ == "__main__":
    t = Tree(decision_state=True)
    t.actions[0].insert_observation(0)
    #t.actions[1].insert_observation(0)
    t.printTree()
