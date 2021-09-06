"""
Experiments for time of algos with ranker count
Datset is for the mediumFair scenario as presented in table 1
"""

#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>

import sys
import time

# append the path of the parent directory

import multi_fair as mf
import numpy as np
import pandas as pd




data_filenames = [r"R100.csv",
                  r"R1000.csv",
                  r"R10000.csv",
                  r"R100000.csv"]

outputfile = r"Malowsresults_rankertime_mediumfair.csv"

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

#data collectors
gender = []
race = []
intersection = []
method = []
runtime = []
rankings = []
rankers = [100, 1000, 10000, 100000, 1000000, 10000000]


for i in range(0, len(data_filenames)+2):

    if i == 4:
        #one million
        data_filename = r"R100000.csv"
        tenk_base_ranks = np.genfromtxt(data_filename, delimiter=',', dtype=int)
        one_million = np.repeat(tenk_base_ranks, 10, 0)
        base_ranks = one_million
    if i == 5:
        # ten million
        data_filename = r"R100000.csv"
        tenk_base_ranks = np.genfromtxt(data_filename, delimiter=',', dtype=int)
        ten_million = np.repeat(tenk_base_ranks, 100, 0)
        base_ranks = ten_million
    if i < 4:
        base_ranks = np.genfromtxt(data_filenames[i], delimiter=',', dtype=int)

    ###############
    # Post Correction
    ##############



    #################
    # Borda+ post correct
    start_time = time.time()
    borda_soln = mf.borda(base_ranks)  # borda +post correct
    greedy_soln = mf.correct_parity(np.asarray(borda_soln), groups_key, pthresh_vals, ithresh)
    end_time = time.time()
    total_time = end_time - start_time
    runtime.append(total_time)
    method.append("borda + post_correct")
    rankings.append(rankers[i])
    print("borda + post time", total_time)
    print("post_correct", i, "done")

    # attribute 1 parity
    fpr_a1 = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[1])))
    gender.append(mf.rank_parity_score(fpr_a1))

    # attribute 2 parity
    fpr_a2 = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[2])))
    race.append(mf.rank_parity_score(fpr_a2))

    # intersectional parity
    fpr_inter = mf.fpr(greedy_soln, np.row_stack((groups_all_key[0], groups_all_key[3])))
    intersection.append(mf.rank_parity_score(fpr_inter))


    # intermediate results
    # dictionary of lists
    dict = {'time': runtime, 'method': method, 'maxdifparity_gender': gender, 'maxdifparity_race': race,
            'maxdifparity_intersectional': intersection, "ranker_num": rankings}

    results = pd.DataFrame(dict)
    print(results)
    results.to_csv(outputfile, index=False)

# dictionary of lists
dict = {'time': runtime, 'method': method, 'maxdifparity_gender': gender, 'maxdifparity_race': race,
            'maxdifparity_intersectional': intersection, "ranker_num": rankings}

results = pd.DataFrame(dict)
print(results)
results.to_csv(outputfile, index=False)
