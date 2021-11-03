"""
Borda Rankings Experiment
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

def run_rankerevaluation_of_methods():
    rankers = [1000, 10000, 100000, 1000000, 10000000]
    data_filenames = [r"R1000.csv",
                      r"R10000.csv"]

    # data collectors
    gender_arp = []
    race_arp = []
    intersection_irp = []
    method = []
    runtime = []
    num_baserankings = []

    #group/algo information
    pthres = [.1, .1]
    ithres = .1
    NUM_GROUPS = 2 * 2
    GRP_SZ = 25
    atr1 = np.hstack((np.zeros(50, dtype=int), np.ones(50, dtype=int)))
    atr2 = np.tile((0, 1, 2, 3, 4), 20)
    groups = np.row_stack((atr1, atr2))
    items_m = np.arange(0, GRP_SZ * NUM_GROUPS)
    group_info = np.row_stack((items_m, groups))
    intersectional = mf.make_intersectional_attribute(group_info, True)
    groups_inter = np.row_stack((items_m, intersectional))
    groups_info_with_inter = np.row_stack((group_info, intersectional))
    for i in range(0, len(data_filenames)+2):

        if i == 2:
            # 1000k
            data_filename = r"R10000.csv"
            tenk_base_ranks = np.genfromtxt(data_filename, delimiter=',', dtype=int)
            hundred = np.repeat(tenk_base_ranks, 10, 0)
            base_ranks = hundred

        if i == 3:
            # one million
            data_filename = r"R10000.csv"
            tenk_base_ranks = np.genfromtxt(data_filename, delimiter=',', dtype=int)
            one_million = np.repeat(tenk_base_ranks, 100, 0)
            base_ranks = one_million
        if i == 4:
            # ten million
            data_filename = r"R10000.csv"
            tenk_base_ranks = np.genfromtxt(data_filename, delimiter=',', dtype=int)
            ten_million = np.repeat(tenk_base_ranks, 1000, 0)
            base_ranks = ten_million
        if i < 3:
            base_ranks = np.genfromtxt(data_filenames[i], delimiter=',', dtype=int)


        outputfile = "Borda_rankerscale_results.csv"

        # FAIR BORDA
        start_time = time.time()
        fair_soln = mf.fair_borda(base_ranks, groups_info_with_inter, pthres, ithres)
        end_time = time.time()
        total_time = end_time - start_time
        print("borda", i)

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
        num_baserankings.append(rankers[i])


        # dictionary of lists
        dict = {'runtime': runtime, 'method': method, 'gender_arp': gender_arp, 'race_arp': race_arp,
                'intersection_irp': intersection_irp, "num_baserankings": num_baserankings}

        results = pd.DataFrame(dict)
        print(results)
        results.to_csv(outputfile, index=False)

run_rankerevaluation_of_methods()



