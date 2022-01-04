import gym_pomdp.envs.rock as pkg
from copy import deepcopy
from POMCP import POMCP


if __name__ == '__main__':

    # initiating game
    env = pkg.RockEnv(board_size=4, num_rocks=3, use_heuristic=False)
    ob = env.reset()
    simulator = deepcopy(env)

    agent = POMCP(simulator=simulator)
    # pay attention to gamma=0.3, epsilon=0.001 and C for exploration !! parameters

    # Start game
    r = 0
    discount = 1.
    hist = []
    for i in range(400):
        print("History so far : ", hist)

        # search and play the best action
        action = agent.search(hist)
        next_ob, rw, done, info = env.step(action)

        # update history
        hist.append(action)
        hist.append(next_ob)

        # rebase tree
        agent.rebase_tree(action, next_ob)

        r += rw * discount
        discount *= env._discount
        if done:
            break
    # End game
    print(r)
