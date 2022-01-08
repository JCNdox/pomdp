import numpy as np
from gym_pomdp.envs import rock
from copy import deepcopy
import gym_pomdp.envs.rock as pkg

# Skeleton code
from Tree2 import Tree2


class POMCP:
    """
    Partially Observable Monte-Carlo Planning
    """

    def __init__(self, gamma=0.3, epsilon=0.001, simulator=None, number_of_simulations=100):
        self.gamma = gamma
        self.epsilon = epsilon
        self.number_of_simulations = number_of_simulations
        self.tree = None
        self.simulator = simulator  # Black box simulator

    def rebase_tree(self, action, observation):
        """
        rebase the tree of the agent when the agent has played his move and obtained the observation (tree pruning).
        :param action: action played by the agent
        :param observation: observation obtained by playing this action
        """
        new_root = self.tree.get_leading_state(action)
        new_root = new_root.get_leading_state(observation)
        self.tree = new_root

    def search(self, history):
        """
        Starting from a history, this function will sample a state from either the initial states or the Belief states
        then it will construct a search tree by doing some simulations. At the end it will return the best move for that
        history.
        :param history: the current sequence of actions and observations that the agent has
        :return: the best action for the agent according to the history.
        """
        for simulation in range(self.number_of_simulations):
            if len(history) == 0:
                # sample an initial state
                self.simulator.reset()          # new game
                state = self.simulator.get_state()  # new initial state
                # self.simulator.print_state(state)
            else:
                # sample from Belief state
                state = np.random.choice(self.tree.get_belief_state())
                self.simulator.set_state(state)    # putting the state in the simulator

            # start simulation from this history
            si = self.simulate(state, [], 0)
            # print("Simulation return  = ", si)
        # print(self.tree.printTree())

        # playing the best move
        best_action = self.tree.real_actions[np.argmax(self.tree.next_state_values(0))]
        return best_action

    def get_node(self, h):
        """
        Starting from a history h, this function search if this sequence of actions and observations has already been
        explore by the agent or not. In the first case it will return true and the node/state of the agent otherwise it
        returns False and the last node or the tree according to the history
        :param h: history
        :return: state and boolean
        """
        node_in_tree = False
        node = self.tree
        if node is not None:
            node_in_tree = True
            for elem in h:
                if node.contains(elem):
                    node = node.get_leading_state(elem)
                else:
                    node_in_tree = False
                    break
        return node, node_in_tree

    def simulate(self, state, history, depth):
        """
        This function will run a simulation of the game. It will choose action randomly out the tree and in the tree it
        will use the tree policy. At the end the function will update the tree counters and return the reward we got by
        playing this sequence of actions.
        :param state:
        :param history:
        :param depth:
        :return:
        """
        if self.gamma ** depth < self.epsilon or self.simulator.done:
            # End of simulation
            return 0

        node, in_tree = self.get_node(history)
        if not in_tree:
            moves = self.simulator.get_possible_actions()
            if node is None:
                # building a tree
                self.tree = Tree2()
                for action in moves:
                    self.tree.add_child(action)
            else:
                # extend tree
                node.add_observation(history[-1])
                node = node.get_leading_state(history[-1])
                for action in moves:
                    node.add_child(action)

            # playing OUT OF THE TREE policy (random play)
            return self.rollout(deepcopy(state), deepcopy(history), depth)

        # playing IN THE TREE policy (tree policy)
        a = node.tree_policy()
        # playing this move will lead you to new state s2 + reward r + observation o
        self.simulator.set_state(deepcopy(state))
        next_ob, rw, done, info = self.simulator.step(a)
        history.append(a)
        history.append(next_ob)
        R = rw + self.gamma * self.simulate(info['state'], history, depth+1)

        # update the nodes counters ....
        node.add_to_belief_state(deepcopy(state))
        node.increment_state_counter()
        node.increment_action_counter(a)
        node.increment_next_state_value(a, R)
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
        if self.gamma ** depth < self.epsilon or self.simulator.done:
            # end of simulation
            return 0

        # otherwise keep playing randomly
        self.simulator.set_state(state)
        a = np.random.choice(self.simulator.get_possible_actions())

        # playing this move will lead you to new state s2 + reward r + observation o
        next_ob, rw, done, info = self.simulator.step(a)
        return rw + self.gamma * self.rollout(info['state'], history, depth + 1)


# test game (see RockGame.py for the experiment)
if __name__ == '__main__':
    history = pkg.History()

    # initiating game
    env = pkg.RockEnv(board_size=4, num_rocks=3, use_heuristic=False)
    ob = env.reset()
    simulator = deepcopy(env)

    agent = POMCP(gamma=1, simulator=simulator, number_of_simulations=500)
    # pay attention to gamma=0.3, epsilon=0.001 and C for exploration !! parameters

    # starting the game gui
    env.render()
    r = 0
    discount = 1.
    hist = []

    for i in range(400):

        print("History so far : ", hist)
        #print("Game state = ", env._encode_state(env.state))
        action = agent.search(hist)

        ###############################################
        # in order to play your self
        print("Play one move in = ", env.get_possible_actions())
        action = int(input())
        next_ob, rw, done, info = env.step(action)
        ob = next_ob
        history.append(pkg.Transition(ob, action, next_ob, rw, done))
        ###############################################

        hist.append(action)
        hist.append(ob)

        env.render()
        r += rw * discount
        discount *= env._discount

        if done:
            break
        else:
            # rebase tree
            agent.rebase_tree(action, ob)
    # End game
    print(r)
