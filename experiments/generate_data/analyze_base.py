import pandas as pd
import numpy as np
import multi_fair as mf


data_filenames = ['/Users/KathleenCachel/OneDrive - Worcester Polytechnic Institute (wpi.edu)/PycharmProjects/multi_fair_rank_agg/experiments/generate_data/Rtheta_8lotsatr.csv']
base_ranks = np.genfromtxt(data_filenames[0], delimiter=',', dtype=int)
outputfile = 'analyzeranking.csv'

NUM_GROUPS = 15
GRP_SZ = 6
atr1 = np.hstack((np.zeros(30, dtype=int), np.ones(30, dtype=int),np.ones(30, dtype=int)*2))
atr2 = np.tile((0, 1, 2, 3, 4), 18)
atr3 = np.tile((0,1), 45)
atr4 = np.hstack((np.zeros(30, dtype=int), np.ones(30, dtype=int),np.ones(30, dtype=int)*2))
groups = np.row_stack((atr1, atr2, atr3, atr4))
items = np.arange(0, GRP_SZ*NUM_GROUPS)

groups = np.row_stack((items, groups))
intersectional = mf.make_intersectional_attribute(groups, True)
groups_inter = np.row_stack((items, intersectional))
groups_all_key = np.row_stack((groups, intersectional))


atr1 = []
atr2 = []
atr3 = []
atr4 = []
inter = []
rank_num = []

for i in range(base_ranks.shape[0]):
    ranking = base_ranks[i, :]

    rank_num.append(i)
    fpr_a1 = mf.fpr(ranking, np.row_stack((groups[0], groups[1])))
    print("FPR ", fpr_a1)
    print("ARP ", mf.rank_parity_score(fpr_a1))
    atr1.append(mf.rank_parity_score(fpr_a1))

    # groups_for_atr2 = ranking_with_group_labels(soln, groups[0], groups[2])
    fpr_a2 = mf.fpr(ranking, np.row_stack((groups[0], groups[2])))
    print("FPR ", fpr_a2)
    print("ARP ", mf.rank_parity_score(fpr_a2))
    atr2.append(mf.rank_parity_score(fpr_a2))

    fpr_a3 = mf.fpr(ranking, np.row_stack((groups[0], groups[3])))
    print("FPR ", fpr_a3)
    print("ARP ", mf.rank_parity_score(fpr_a3))
    atr3.append(mf.rank_parity_score(fpr_a3))

    fpr_a4 = mf.fpr(ranking, np.row_stack((groups[0], groups[4])))
    print("FPR ", fpr_a4)
    print("ARP ", mf.rank_parity_score(fpr_a4))
    atr4.append(mf.rank_parity_score(fpr_a4))

    fpr_intersectional = mf.fpr(ranking, np.row_stack((groups[0], groups_all_key[5])))
    print("FPR ", fpr_intersectional)
    print("IRP ", mf.rank_parity_score(fpr_intersectional))
    inter.append(mf.rank_parity_score(fpr_intersectional))



dict = {'atr1': atr1, 'atr2': atr2, 'atr3': atr3, 'atr4': atr4, 'inter': inter,
        'rank_num': rank_num}

results = pd.DataFrame(dict)
print(results)
results.to_csv(outputfile, index=False)