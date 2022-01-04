import numpy as np
from gym_pomdp.envs import rock
from copy import deepcopy
import gym_pomdp.envs.rock as pkg

# Skeleton code
from Tree import Tree
from Tree2 import Tree2


class POMCP:

    def __init__(self, gamma=0.3, epsilon=0.001, number_actions=4, simulator=None, number_of_simulations=100):
        self.gamma = gamma
        self.epsilon = epsilon
        self.number_of_actions = number_actions
        self.number_of_simulations = number_of_simulations
        self.tree = None
        self.history = []
        self.simulator = simulator

    def rebase_tree(self, action, observation):
        new_root = self.tree.get_leading_state(action)
        new_root = new_root.get_leading_state(observation)
        self.tree = new_root

    def belief_state(self, history):
        self.simulator.reset()
        print("playing : ", history)
        for action in range(0, len(history), 2):
            self.simulator.step(history[action])
        state = self.simulator.state
        return self.simulator._encode_state(state)

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
                self.simulator.reset()
                state = self.simulator._encode_state(self.simulator.state)
            else:
                # sample from Belief state
                state = np.random.choice(agent.tree.get_belief_state())
            # start simulation from this history
            print("Simulation return  = ", self.simulate(state, [], 0))
            print(agent.tree.printTree())

        # playing the best move
        best_action = agent.tree.real_actions[np.argmax(agent.tree.next_state_values(0))]
        print("Best action", best_action)
        #print("search = ", state)
        # rebase tree !!
        return best_action

    def get_node(self, h):
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
            moves = self.simulator._generate_legal()
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
            return self.rollout(state, history, depth)

        # playing IN THE TREE policy (greedy with exploration)
        #print(agent.tree.printTree())

        a = node.tree_policy()
        # playing this move will lead you to new state s2 + reward r + observation o
        self.simulator._set_state(state)
        next_ob, rw, done, info = self.simulator.step(a)
        history.append(a)
        history.append(next_ob)
        R = rw + self.gamma * self.simulate(info['state'], history, depth+1)

        # update the nodes counters ....
        node.add_to_belief_state(state)
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
        if self.gamma ** depth < self.epsilon:
            # end of simulation
            return 0

        # otherwise keep playing randomly
        self.simulator._set_state(state)
        a = np.random.choice(self.simulator._generate_legal())
        # playing this move will lead you to new state s2 + reward r + observation o
        next_ob, rw, done, info = self.simulator.step(a)
        history.append(a)
        history.append(next_ob)
        return rw + self.gamma * self.rollout(info['state'], history, depth + 1)


if __name__ == '__main__':
    history = pkg.History()
    env = pkg.RockEnv(board_size=4, num_rocks=3, use_heuristic=False)
    ob = env.reset()
    simulator = deepcopy(env)
    env.render()
    r = 0
    discount = 1.
    agent = POMCP(simulator=simulator)
    hist = []
    #agent.search(deepcopy(hist))
    #print(agent.tree.printTree())
    for i in range(400):

        print("History so far : ", hist)
        action = agent.search(deepcopy(hist))


        ###############################################
        print("Play one move in = ", env._generate_legal())
        action = int(input())
        next_ob, rw, done, info = env.step(action)
        ob = next_ob
        history.append(pkg.Transition(ob, action, next_ob, rw, done))
        ###############################################

        hist.append(action)
        hist.append(ob)
        # rebase tree
        agent.rebase_tree(action, ob)
        #print("Rebased tree : ")
        #print(agent.tree.printTree())

        #print(next_ob, rw, done, info['state'])
        env.render()
        r += rw * discount
        discount *= env._discount

        if done:
            break
    print(r)
