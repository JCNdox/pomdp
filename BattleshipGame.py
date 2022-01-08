import gym_pomdp.envs.battleship as pkg
from POMCP import POMCP
from copy import deepcopy
if __name__ == "__main__":

    env = pkg.BattleShipEnv()
    ob = env.reset()

    simulator = deepcopy(env)
    agent = POMCP(gamma=1, simulator=simulator, number_of_simulations=500)
    hist = []

    env.render()
    done = False
    t = 0

    while not done:
        print("History so far : ", hist)

        # search and play the best action
        action = agent.search(hist)

        #print("Remaining ships = ", env.state.total_remaining)
        print("Play = ", env.state.remaining_actions)

        #action = int(input())

        ob, rw, done, info = env.step(action)
        print(ob, rw, done, info, info['state'].total_remaining)



        # update history
        hist.append(action)
        hist.append(ob)

        # rebase tree if game not done
        if not done:
            agent.rebase_tree(action, ob)

        # initiating the simulator

        env.render()
        t += 1
    env.close()

    print("rw {}, t{}".format(rw, t))
