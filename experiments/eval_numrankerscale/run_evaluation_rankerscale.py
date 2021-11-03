"""
Script for evaluating non-Optimization methods on Mallows datasets
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

def run_rankerevaluation_of_methods(method_type):
    rankers = [100, 500, 1000, 5000, 10000, 20000]
    data_filenames = [r"R100.csv",
                      r"R500.csv",
                      r"R1000.csv",
                      r"R5000.csv",
                      r"R10000.csv"]

    # data collectors
    method = []
    runtime = []
    num_baserankings = []


    #group/algo information
    pthres = [.1, .1]
    ithres = .1
    thresh_fairilp = [.1, .1, .1]
    NUM_GROUPS = 2 * 5
    GRP_SZ = 10
    atr1_m = np.hstack((np.zeros(50, dtype=int), np.ones(50, dtype=int)))
    atr2_m = np.tile((0, 1, 2, 3, 4), 20)
    groups = np.row_stack((atr1_m, atr2_m))
    items_m = np.arange(0, GRP_SZ * NUM_GROUPS)
    group_info = np.row_stack((items_m, groups))
    intersectional = mf.make_intersectional_attribute(group_info, True)
    groups_inter = np.row_stack((items_m, intersectional))
    groups_info_with_inter = np.row_stack((group_info, intersectional))
    for i in range(0, len(rankers)):


        if i == 5:
            # 20k
            data_filename = r"R10000.csv"
            tenk_base_ranks = np.genfromtxt(data_filename, delimiter=',', dtype=int)
            twentyk = np.repeat(tenk_base_ranks, 2, 0)
            base_ranks = twentyk
        if i < 5:
            base_ranks = np.genfromtxt(data_filenames[i], delimiter=',', dtype=int)


        if method_type == "IP":
            #optimization methods
            outputfile = "IP_rankerscale_results.csv"
            # KEMENY
            start_time = time.time()
            prob_result = mf.aggregate_rankings(base_ranks)
            kemeny_soln = mf.find_solution(prob_result, GRP_SZ * NUM_GROUPS)
            end_time = time.time()
            total_time = end_time - start_time
            print("kemeny", kemeny_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(kemeny_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(kemeny_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(kemeny_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)

            method.append("Kemeny")
            runtime.append(total_time)
            num_baserankings.append(rankers[i])

            # WEIGHTED KEMENY
            start_time = time.time()
            fair_soln = mf.weight_kemeny_fair(base_ranks, groups_info_with_inter, pthres, ithres, True)
            end_time = time.time()
            total_time = end_time - start_time
            print("weighted kemeny", fair_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Weighted_Kemeny")
            runtime.append(total_time)
            num_baserankings.append(rankers[i])

            # FAIR ILP
            start_time = time.time()
            prob_result = mf.aggregate_rankings_fair_ilp(base_ranks, groups_info_with_inter, thresh_fairilp, True)
            fair_soln = mf.find_solution(prob_result, GRP_SZ * NUM_GROUPS)
            end_time = time.time()
            total_time = end_time - start_time
            print("fair ilp", fair_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Fair_Kemeny")
            runtime.append(total_time)
            num_baserankings.append(rankers[i])

            # dictionary of lists
            dict = {'runtime': runtime, 'method': method, "num_baserankings": num_baserankings}

            results = pd.DataFrame(dict)
            print(results)
            results.to_csv(outputfile, index=False)


        if method_type == "foot":
            #non optimization methods
            outputfile = "footrule_rankerscale_results.csv"

            # FAIR FOOTRULE
            start_time = time.time()
            prob_result = mf.aggregate_footrule(base_ranks, groups_info_with_inter, thresh_fairilp, True)
            fair_soln = mf.find_solution(prob_result, num_items)
            end_time = time.time()
            total_time = end_time - start_time
            print("fair footrule")

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Fair_Footrule")
            runtime.append(total_time)
            num_baserankings.append(rankers[i])

            # dictionary of lists
            dict = {'runtime': runtime, 'method': method, "num_baserankings": num_baserankings}

            results = pd.DataFrame(dict)
            print(results)
            results.to_csv(outputfile, index=False)


        if method_type == "NOIP":
            #non optimization methods
            outputfile = "NOIP_rankerscale_results.csv"

            # FAIR SCHULZE
            start_time = time.time()
            fair_soln = mf.fair_schulze(base_ranks, groups_info_with_inter, pthres, ithres)
            end_time = time.time()
            total_time = end_time - start_time
            print("schulze", fair_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Fair_Schulze")
            runtime.append(total_time)
            num_baserankings.append(rankers[i])


            # FAIR BORDA
            start_time = time.time()
            fair_soln = mf.fair_borda(base_ranks, groups_info_with_inter, pthres, ithres)
            end_time = time.time()
            total_time = end_time - start_time
            print("borda", fair_soln)

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
            runtime.append(total_time)
            num_baserankings.append(rankers[i])

            # FAIR COPELAND
            start_time = time.time()
            fair_soln = mf.fair_copeland(base_ranks, groups_info_with_inter, pthres, ithres)
            end_time = time.time()
            total_time = end_time - start_time
            print("COPELAND", fair_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Fair_Copeland")
            runtime.append(total_time)
            num_baserankings.append(rankers[i])

            # PICK FAIREST PERM
            start_time = time.time()
            fair_soln = mf.pick_fairest_perm(base_ranks, groups_info_with_inter, pthres, ithres, True)
            end_time = time.time()
            total_time = end_time - start_time
            print("pick fairest perm", fair_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Pick_Fairest_Perm")
            runtime.append(total_time)
            num_baserankings.append(rankers[i])

            # CORRECT FAIREST PERM
            start_time = time.time()
            fair_soln = mf.correct_fairest_perm(base_ranks, groups_info_with_inter, pthres, ithres, True)
            end_time = time.time()
            total_time = end_time - start_time
            print("correct fairest perm", fair_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)

            method.append("Correct_Fairest_Perm")
            runtime.append(total_time)
            num_baserankings.append(rankers[i])

            # dictionary of lists
            dict = {'runtime': runtime, 'method': method, "num_baserankings": num_baserankings}

            results = pd.DataFrame(dict)
            print(results)
            results.to_csv(outputfile, index=False)
run_rankerevaluation_of_methods("NOIP")
run_rankerevaluation_of_methods("IP")



