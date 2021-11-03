"""
Script for evaluating fair-borda on number of candidates
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
import sys
import time

def run_candidatenum_evaluation_of_borda():

    candidates = [1000, 10000, 20000, 30000, 40000, 50000, 100000]
    data_filenames = [r"N1000.npy",
                      r"N10000.npy",
                      r"N20000.npy",
                      r"N30000.npy",
                      r"N40000.npy",
                      r"N50000.npy",
                      r"N100000.npy"]
    # data collectors
    gender_arp = []
    race_arp = []
    intersection_irp = []
    method = []
    runtime = []
    num_candidates = []


    #group/algo information
    pthres = [.33, .33]
    ithres = .33
    NUM_GROUPS = 25
    GRP_SZ = 4
    atr1_m = np.hstack((np.zeros(50, dtype=int), np.ones(50, dtype=int)))
    atr2_m = np.tile(range(0, 2), 50)
    groups = np.row_stack((atr1_m, atr2_m))
    items_m = np.arange(0, GRP_SZ * NUM_GROUPS)
    group_info = np.row_stack((items_m, groups))
    intersectional = mf.make_intersectional_attribute(group_info, True)
    groups_inter = np.row_stack((items_m, intersectional))
    groups_info_with_inter = np.row_stack((group_info, intersectional))
    for i in range(0, len(data_filenames)):

        base_ranks = np.load(data_filenames[i])
        num_rankers, num_items = base_ranks.shape
        scale_factor = int(num_items / 100)
        # adjust group key
        atr_1 = np.tile(atr1_m, scale_factor)
        atr_2 = np.tile(atr2_m, scale_factor)
        groups = np.row_stack((atr_1, atr_2))
        items = np.arange(0, num_items)
        group_info = np.row_stack((items, groups))
        intersectional = mf.make_intersectional_attribute(group_info, False)
        groups_info_with_inter = np.row_stack((group_info, intersectional))

        #non optimization methods
        outputfile = "borda_candidatescale_results.csv"

        # FAIR BORDA
        start_time = time.time()
        fair_soln = mf.fair_borda(base_ranks, groups_info_with_inter, pthres, ithres)
        end_time = time.time()
        total_time = end_time - start_time
        print("borda", candidates[i])

        # attribute 1 parity
        fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
        ARP_a1 = mf.rank_parity_score(fpr_a1)

        # attribute 2 parity
        fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
        ARP_a2 = mf.rank_parity_score(fpr_a2)

        # intersectional parity
        FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
        irp_val = mf.rank_parity_score(FPR_inter)
        method.append("Fair_Borda")
        gender_arp.append(ARP_a1)
        race_arp.append(ARP_a2)
        intersection_irp.append(irp_val)
        runtime.append(total_time)
        num_candidates.append(candidates[i])


        # dictionary of lists
        dict = {'runtime': runtime, 'method': method, 'gender_arp': gender_arp, 'race_arp': race_arp,
                'intersection_irp': intersection_irp, "num_candidates": num_candidates}

        results = pd.DataFrame(dict)
        print(results)
        #results.to_csv(outputfile, index=False)

run_candidatenum_evaluation_of_borda()



