"""
Script for evaluating methods on number of candidates
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

def run_candidatenum_evaluation_of_methods(method_type):

    candidates = [100, 200, 260,300, 400, 500]
    data_filenames = [r"N100.npy",
                       r"N200.npy",
                       r"N260.npy",
                       r"N300.npy",
                       r"N400.npy",
                       r"N500.npy"]


    # data collectors
    method = []
    runtime = []
    num_candidates = []
    threshold = []


    #group/algo information
    for t in range(0,2):
        if t == 0:
            pthres = [.1, .1]
            ithres = .1
            thresh_fairilp = [.1, .1, .1]
        if t == 1:
            pthres = [.33, .33]
            ithres = .33
            thresh_fairilp = [.33, .33, .33]

        NUM_GROUPS = 25
        GRP_SZ = 4
        atr1_m = np.hstack((np.zeros(50, dtype=int), np.ones(50, dtype=int)))
        atr2_m = np.tile(range(0, 2), 50)
        groups = np.row_stack((atr1_m, atr2_m))
        items_m = np.arange(0, 100)
        group_info = np.row_stack((items_m, groups))
        intersectional = mf.make_intersectional_attribute(group_info, True)
        groups_inter = np.row_stack((items_m, intersectional))
        groups_info_with_inter = np.row_stack((group_info, intersectional))
        for i in range(0, len(data_filenames)):

            base_ranks = np.load(data_filenames[i])
            num_rankers, num_items = base_ranks.shape
            if num_items != 260:
                scale_factor = int(num_items / 100)
                # adjust group key
                atr_1 = np.tile(atr1_m, scale_factor)
                atr_2 = np.tile(atr2_m, scale_factor)
            if num_items == 260:
                atr_1 = np.zeros(260, dtype = int)
                atr_2 = np.zeros(260, dtype=int)
                start = 0
                for x in range(0,100):
                    if x < 60:
                        stop = start + 3
                        atr_1[start:stop] = np.tile(atr1_m[x],3)
                        atr_2[start:stop] = np.tile(atr2_m[x], 3)
                        start = stop
                    if x >= 60:
                        stop = start + 2
                        atr_1[start:stop] = np.tile(atr1_m[x], 2)
                        atr_2[start:stop] = np.tile(atr2_m[x], 2)
                        start = stop

            groups = np.row_stack((atr_1, atr_2))
            items = np.arange(0, num_items)
            group_info = np.row_stack((items, groups))
            intersectional = mf.make_intersectional_attribute(group_info, False)
            groups_info_with_inter = np.row_stack((group_info, intersectional))


            if method_type == "IP":
                #optimization methods
                outputfile = "IP_candidatescale_results.csv"

                # FAIR ILP
                start_time = time.time()
                prob_result = mf.aggregate_rankings_fair_ilp(base_ranks, groups_info_with_inter, thresh_fairilp, True)
                fair_soln = mf.find_solution(prob_result, num_items)
                end_time = time.time()
                total_time = end_time - start_time
                print("fair ilp", candidates[i])

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
                num_candidates.append(candidates[i])
                threshold.append(ithres)

                # dictionary of lists
                dict = {'runtime': runtime, 'method': method, "num_candidates": num_candidates, 'threshold': threshold}

                results = pd.DataFrame(dict)
                print(results)
                results.to_csv(outputfile, index=False)

                #KEMENY
                start_time = time.time()
                prob_result = mf.aggregate_rankings(base_ranks)
                kemeny_soln = mf.find_solution(prob_result, num_items)
                end_time = time.time()
                total_time = end_time - start_time
                print("kemeny", candidates[i])

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
                num_candidates.append(candidates[i])
                threshold.append(ithres)

                # dictionary of lists
                dict = {'runtime': runtime, 'method': method, "num_candidates": num_candidates, 'threshold': threshold}

                results = pd.DataFrame(dict)
                print(results)
                results.to_csv(outputfile, index=False)



                # WEIGHTED KEMENY
                start_time = time.time()
                fair_soln = mf.weight_kemeny_fair(base_ranks, groups_info_with_inter, pthres, ithres, True)
                end_time = time.time()
                total_time = end_time - start_time
                print("weighted kemeny", candidates[i])

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
                num_candidates.append(candidates[i])
                threshold.append(ithres)

                # dictionary of lists
                dict = {'runtime': runtime, 'method': method, "num_candidates": num_candidates, 'threshold': threshold}

                results = pd.DataFrame(dict)
                print(results)
                results.to_csv(outputfile, index=False)





            if method_type == "NOIP":
                #non optimization methods
                outputfile = "NOIP_candidatescale_results.csv"

                # FAIR SCHULZE
                start_time = time.time()
                fair_soln = mf.fair_schulze(base_ranks, groups_info_with_inter, pthres, ithres)
                end_time = time.time()
                total_time = end_time - start_time
                print("schulze", candidates[i])

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
                num_candidates.append(candidates[i])
                threshold.append(ithres)


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
                runtime.append(total_time)
                num_candidates.append(candidates[i])
                threshold.append(ithres)

                # FAIR COPELAND
                start_time = time.time()
                fair_soln = mf.fair_copeland(base_ranks, groups_info_with_inter, pthres, ithres)
                end_time = time.time()
                total_time = end_time - start_time
                print("COPELAND", candidates[i])

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
                num_candidates.append(candidates[i])
                threshold.append(ithres)



                # PICK FAIREST PERM
                start_time = time.time()
                fair_soln = mf.pick_fairest_perm(base_ranks, groups_info_with_inter, pthres, ithres, True)
                end_time = time.time()
                total_time = end_time - start_time
                print("pick fairest perm", candidates[i])

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
                num_candidates.append(candidates[i])
                threshold.append(ithres)

                # CORRECT FAIREST PERM
                start_time = time.time()
                fair_soln = mf.correct_fairest_perm(base_ranks, groups_info_with_inter, pthres, ithres, True)
                end_time = time.time()
                total_time = end_time - start_time
                print("correct fairest perm", candidates[i])

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
                num_candidates.append(candidates[i])
                threshold.append(ithres)

                # dictionary of lists
                dict = {'runtime': runtime, 'method': method, "num_candidates": num_candidates, 'threshold': threshold}

                results = pd.DataFrame(dict)
                print(results)
                results.to_csv(outputfile, index=False)


run_candidatenum_evaluation_of_methods("IP")
run_candidatenum_evaluation_of_methods("NOIP")




