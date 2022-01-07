import gym_pomdp.envs.rock as pkg
from copy import deepcopy
from POMCP import POMCP
import numpy as np
from time import time
import matplotlib.pyplot as plt


if __name__ == '__main__':

    nbr_of_runs = 10 #20
    nbr_of_sim = [200, 400, 600, 800, 1000]
    gammas = [0.30, 0.60, 0.95]
    count = np.zeros(len(nbr_of_sim) * len(gammas)).reshape(len(gammas), len(nbr_of_sim))
    j = 0
    all_start = time()
    for gamma in gammas:
        k = 0
        start = time()
        for nbr in nbr_of_sim:
            nbr_of_success = 0
            for i in range(nbr_of_runs):
                try:
                    hist = []
                    env = pkg.RockEnv(board_size=7, num_rocks=8, use_heuristic=False)
                    ob = env.reset()
                    simulator = deepcopy(env)
                    agent = POMCP(simulator=simulator, number_of_simulations=nbr, gamma=gamma)
                    r = 0
                    discount = 1.
                    hist = []
                    done = False
                    while not done:
                        action = agent.search(hist)
                        next_ob, rw, done, info = env.step(action)
                        hist.append(action)
                        hist.append(next_ob)
                        r += rw * discount
                        discount *= env._discount
                        if not done:
                            agent.rebase_tree(action, next_ob)
                    nbr_of_success += 1
                    count[j][k] += r
                except:
                    pass

            print("Nbr of success for gamma = ", gamma, " with ", nbr, " simulations : ", nbr_of_success)
            count[j][k]/=(nbr_of_success)
            
            k+=1
        end = time() - start
        print("Time = ", end, " sec with gamma = ", gammas[j])
        j+=1

    all_end = time() - all_start
    print("Total time = ", all_end)
    print(count)
    for i in range(len(gammas)):
        plt.plot(nbr_of_sim, count[i], marker='o', label="gamma = " + str(gammas[i]))
    plt.xlabel("Number of simulations")
    plt.ylabel("Averaged discouteded return")
    plt.legend()
    plt.show()
