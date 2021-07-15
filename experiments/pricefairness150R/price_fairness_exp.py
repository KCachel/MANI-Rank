"""
Script for Price of Fairness Experiment
"""

#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>
# Authors: Kathleen Cachel <kcachel@wpi.edu>
import sys

# append the path of the parent directory
sys.path.append("..")
import multi_fair as mf
import numpy as np
import pandas as pd




data_filenames = [r"\lowf\Rtheta_2.csv",
                  r"\lowf\Rtheta_4.csv",
                  r"\lowf\Rtheta_6.csv",
                  r"\lowf\Rtheta_8.csv",
                  r"\medf\Rtheta_2.csv",
                  r"\medf\Rtheta_4.csv",
                  r"\medf\Rtheta_6.csv",
                  r"\medf\Rtheta_8.csv",
                  r"\highf\Rtheta_2.csv",
                  r"\highf\Rtheta_4.csv",
                  r"\highf\Rtheta_6.csv",
                  r"\highf\Rtheta_8.csv"]
levels = ['lowf','lowf','lowf','lowf', 'medf', 'medf', 'medf', 'medf', 'highf', 'highf', 'highf', 'highf']
thetas = [.2, .4, .6, .8, .2, .4, .6, .8, .2, .4, .6, .8]
outputfile = r"Malowsresults_150r_pricefairness.csv"



#data collectors
gender = []
race = []
intersection = []
theta = []
method = []
level = []
cf = []




#Create protected attribute information
NUM_GROUPS = 15
GRP_SZ = 6
atr1 = np.hstack((np.zeros(30, dtype=int), np.ones(30, dtype=int), np.ones(30, dtype=int) * 2))
atr2 = np.tile((0, 1, 2, 3, 4), 18)
groups = np.row_stack((atr1, atr2))
items = np.arange(0, GRP_SZ * NUM_GROUPS)
groups_key = np.row_stack((items, groups))
intersectional = mf.make_intersectional_attribute(groups_key, True)
groups_inter = np.row_stack((items, intersectional))
groups_all_key = np.row_stack((groups_key, intersectional))
thres_vals = [.1, .1, .1]
pthresh_vals = [.1, .1]
ithresh = .1

for i in range(len(thetas)):

    base_ranks = np.genfromtxt(data_filenames[i], delimiter=',', dtype=int)

    ###############
    # Kemeny
    ##############
    prob_result = mf.aggregate_rankings(base_ranks)
    kemeny_soln = mf.find_solution(prob_result, GRP_SZ * NUM_GROUPS)
    method.append("Kemeny")
    theta.append(thetas[i])
    level.append(levels[i])
    cf.append(mf.cost_fairness(base_ranks, kemeny_soln, kemeny_soln))
    print("Kemeny ", i, "done")

    # attribute 1 parity
    fpr_a1 = mf.fpr(kemeny_soln, np.row_stack((groups_key[0], groups_key[1])))
    gender.append(mf.rank_parity_score(fpr_a1))

    # attribute 2 parity
    fpr_a2 = mf.fpr(kemeny_soln, np.row_stack((groups_key[0], groups_key[2])))
    race.append(mf.rank_parity_score(fpr_a2))

    # intersectional parity
    fpr_inter = mf.fpr(kemeny_soln, np.row_stack((groups_all_key[0], groups_all_key[3])))
    intersection.append(mf.rank_parity_score(fpr_inter))




    # ###############
    # MFRA-IP
    ##############

    prob_result = mf.aggregate_rankings_fair_ilp(base_ranks, groups_all_key, thres_vals, False)
    fair_soln = mf.find_solution(prob_result, GRP_SZ * NUM_GROUPS)

    cf.append(mf.cost_fairness(base_ranks, kemeny_soln, fair_soln))
    method.append("Fair")
    theta.append(thetas[i])
    level.append(levels[i])
    print("fair ", i, "done")

    # attribute 1 parity
    fpr_a1 = mf.fpr(fair_soln, np.row_stack((groups_key[0], groups_key[1])))
    gender.append(mf.rank_parity_score(fpr_a1))

    # attribute 2 parity
    fpr_a2 = mf.fpr(fair_soln, np.row_stack((groups_key[0], groups_key[2])))
    race.append(mf.rank_parity_score(fpr_a2))

    # intersectional parity
    fpr_inter = mf.fpr(fair_soln, np.row_stack((groups_all_key[0], groups_all_key[3])))
    intersection.append(mf.rank_parity_score(fpr_inter))

    ###############
    # MFRA-PC
    ##############

    greedy_soln = mf.correct_parity(np.asarray(kemeny_soln), groups_key, pthresh_vals, ithresh)
    cf.append(mf.cost_fairness(base_ranks, kemeny_soln, greedy_soln))
    method.append("Greedy_Fair")
    theta.append(thetas[i])
    level.append(levels[i])
    print("greedy fair ", i, "done")

    # attribute 1 parity
    fpr_a1 = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[1])))
    gender.append(mf.rank_parity_score(fpr_a1))

    # attribute 2 parity
    fpr_a2 = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[2])))
    race.append(mf.rank_parity_score(fpr_a2))

    # intersectional parity
    fpr_inter = mf.fpr(greedy_soln, np.row_stack((groups_all_key[0], groups_all_key[3])))
    intersection.append(mf.rank_parity_score(fpr_inter))

    #save progresss
    # dictionary of lists
    dict = {'theta': theta, 'method': method, 'maxdifparity_gender': gender, 'maxdifparity_race': race,
            'level': level, 'maxdifparity_intersectional': intersection, 'cf': cf}
    results = pd.DataFrame(dict)
    print(results)

# dictionary of lists
dict = {'theta': theta, 'method': method, 'maxdifparity_gender': gender, 'maxdifparity_race': race,
        'level': level, 'maxdifparity_intersectional': intersection, 'cf': cf}

results = pd.DataFrame(dict)
print(results)
results.to_csv(outputfile,index=False)

