import numpy as np

# Skeleton code
from Tree import Tree


class POMCP:

    def __init__(self, gamma=0.3, epsilon=0.001, number_actions=4, simulator=None, number_of_simulations=1):
        self.gamma = gamma
        self.epsilon = epsilon
        self.number_of_actions = number_actions
        self.number_of_simulations = number_of_simulations
        self.tree = None
        self.history = []
        self.simulator = simulator

    def search(self, history):
        """
        Starting from a history, this function will sample a state from either the initial states or the Belief states
        then it will construct a search tree by doing some simulations. At the end it will return the best move for that
        history.
        :param history: the current sequence of actions and observations that the agent had
        :return: the best action for the agent according to the history.
        """

        for simulation in range(self.number_of_simulations):
            if len(history) == 0:
                # sample a initial state
                pass
            else:
                # sample from Belief states
                pass
            state = None    # should be remove when above is implemented

            # start simulation from this history
            self.simulate(state, history, 0)

        # playing the best move
        return np.argmax("best_move")

    def history_in_tree(self, h):
        if len(h) == 0 and self.tree is None:
            return False

        pass

    def get_node(self, h):
        node = self.tree
        if self.tree is not None:
            node_in_tree = True
            for i in range(len(h)):
                if i % 2 == 0:
                    # action
                    node = node.actions[h[i]]   # taking an action
                else:
                    # observation
                    pos = node.get_observation_pos(h[i])    # observation state
                    if pos is None:
                        node_in_tree = False
                        break
                    node = node.leading_state[pos]
        else:
            node_in_tree = False
        return node, node_in_tree

    def add_history_in_tree(self):
        pass

    def simulate(self, state, history, depth):
        """
        This function will run a simulation of the game. It will choose action randomly out the tree and in the tree it will
        act greedy. At the end the function will update the tree variables and return the reward we got by playing this
        sequence of actions.
        :param state:
        :param history:
        :param depth:
        :return:
        """
        if self.gamma ** depth < self.epsilon:
            # first end of simulation
            return 0

        node, in_tree = self.get_node(history)

        if not in_tree:
            if node is None:
                # building a tree
                self.tree = Tree(decision_state=True)
            else:
                # extend tree
                node.insert_observation(history[-1])

            # playing OUT OF THE TREE policy (random play)
            return self.rollout(state, history, depth)

        # playing IN THE TREE policy (greedy with exploration)
        a = np.argmax(node.next_state_values())
        # playing this move will lead you to new state s2 + reward r + observation o
        R = r + self.gamma * self.simulate(s2, h + a + o, depth + 1)
        # update the nodes counters ....

        return R

    def rollout(self, state, history, depth):
        """
        This function is used to play outside the tree. Action is chosen randomly. It returns the reward got from the
        simulation.
        :param state: state
        :param history: history
        :param depth: depth
        :return: reward got throughout the simulation
        """
        if self.gamma ** depth < self.epsilon:
            # end of simulation
            return 0

        # otherwise keep playing randomly
        a = np.random.randint(self.number_of_actions)
        # playing this move will lead you to new state s2 + reward r + observation o
        return r + self.gamma * self.rollout(s2, h + a + o, depth + 1)


if __name__ == '__main__':
    print("Hello world ")
