import math
import numpy as np

C = 2


class Tree2:
    """
    This class is used to save needed information about the environment in a tree structure. One tree object
    correspond to one node and one node can have several subtrees.
    """

    def __init__(self, n_init=0, v_init=0, depth=0, observation=False):
        self.state_counter = n_init
        self.state_value = v_init  # state value (Q_value of the state)
        self.depth = depth
        self.observation = observation

        self.real_actions = []  # action to take (in order to play the game)
        self.actions = []  # sub trees (where the real action will lead the agent)

        self.belief_state = []

    def get_state_counter(self):
        return self.state_counter

    def increment_state_counter(self):
        self.state_counter += 1

    def increment_action_counter(self, action):
        """
        Increment the counter of the action played
        :param action: the played action
        """
        next_state = self.get_leading_state(action)
        next_state.increment_state_counter()

    def increment_next_state_value(self, action, r):
        """
        Increment the Q value of the next state. The next state is the one if we take the action 'action' from
        this state. The reward got for that action is r
        :param action: action to get the next state
        :param r: reward got for taking this action
        """
        next_state = self.get_leading_state(action)
        next_state.increment_state_value(r)

    def increment_state_value(self, value):
        """
        Increment the Q value of the current state
        :param value: the cumulated reward got starting from this state
        """
        self.state_value += (value - self.state_value) / self.state_counter

    def get_state_value(self):
        """
        :return: the Q value of the state (state value)
        """
        return self.state_value

    def add_to_belief_state(self, state):
        """
        Update the agent's belief state on the environment for the current agent state
        :param state: a possible environment state
        """
        if len(self.belief_state) == 0:
            self.belief_state.append(state)
        else:
            add = True
            for elem in self.belief_state:
                if state.same_state(elem):
                    # The state is already in the belief states so we should not add it again !
                    add = False
                    break
            if add:
                self.belief_state.append(state)

    def get_belief_state(self):
        return self.belief_state

    def add_child(self, action):
        """
        Add a subtree which can be a state where we should decide to take an action or a state where the agent will
        get an observation. Param action can be an observation obtained or a new action that he can take from the
        current state
        :param action: action/observation
        """
        self.real_actions.append(action)
        self.actions.append(Tree2(observation=True))

    def add_observation(self, observation):
        """
        adding a new node for the observation obtained
        :param observation: observation
        """
        self.real_actions.append(observation)
        self.actions.append(Tree2())

    def get_leading_state(self, action):
        """
        return the state where the agent will end up by taking this action
        :param action: action taken
        :return: next state
        """
        pos = 0
        for child in self.real_actions:
            if child == action:
                break
            pos += 1
        return self.actions[pos]

    def contains(self, action):
        """
        check whether an action or an observation have already been discover from this state
        :param action:
        :return:
        """
        return action in self.real_actions

    def next_state_values(self, exploration):
        """
        Gives You all the Q_values of actions of this state
        :return: list of Q_values (v(ha) for all a)
        """
        values = []
        for node in self.actions:
            Q_value = node.get_state_value() + exploration * math.sqrt(
                np.log(self.get_state_counter()) / (node.get_state_counter()))
            values.append(Q_value)
        return values

    def tree_policy(self):
        """
        Playing the rollout policy until when each move has been played once. After that Play the best move
        with some bonus point if a node has rarely been explored
        :return: the action to play
        """
        if not self.played_all_actions_once():
            return self.real_actions[np.random.randint(0, len(self.actions))]    # Playing the rollout policy in tree
        else:
            return self.real_actions[np.argmax(self.next_state_values(C))]  # playing greedy action + bonus exploration

    def played_all_actions_once(self):
        """
        Check that we have try at least once each actions
        :return: bool true or false
        """
        flag = True
        for action in self.actions:
            if action.get_state_counter() == 0:
                flag = False
                break
        return flag

    def is_observation_node(self):
        """
        :return: true if this node contains observations rather then actions
        """
        return self.observation

    def printTree(self):
        """
        Print the whole tree
        :return:
        """
        if (not self.actions):
            print("empty root")
            return None
        q = []
        print('Root c='+str(self.get_state_counter()))
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
                    print("a"+str(numb)+" c="+str(p.get_state_counter()), end=" ")
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
