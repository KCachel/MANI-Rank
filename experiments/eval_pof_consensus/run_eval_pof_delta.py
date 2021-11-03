"""
Script for pof vs consensus tradeoff with Mallows Model datasets R = 150, n = 90
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

def run_eval_pof_delta(method_type):
    levels = ['lowf','lowf','lowf','lowf', 'medf','medf','medf','medf', 'highf','highf','highf','highf']
    thetas = [.2, .4, .6, .8,.2, .4, .6, .8,.2, .4, .6, .8]
    data_filenames = [r"lowfRtheta_2.csv",
                 r"lowfRtheta_4.csv",
                 r"lowfRtheta_6.csv",
                 r"lowfRtheta_8.csv",
                 r"medfRtheta_2.csv",
                 r"medfRtheta_4.csv",
                 r"medfRtheta_6.csv",
                 r"medfRtheta_8.csv",
                 r"highfRtheta_2.csv",
                 r"highfRtheta_4.csv",
                 r"highfRtheta_6.csv",
                 r"highfRtheta_8.csv",]
    # data collectors
    gender_arp = []
    race_arp = []
    intersection_irp = []
    method = []
    theta_value = []
    dataset = []
    delta = []
    pd_loss = []
    POF_pd = []


    #group/algo information
    pthres_ = [.1, .1]
    ithres_ = .1
    thresh_fairilp_ = [.1, .1, .1]
    NUM_GROUPS = 15
    GRP_SZ = 6
    atr1 = np.hstack((np.zeros(30, dtype=int), np.ones(30, dtype=int), np.ones(30, dtype=int) * 2))
    atr2 = np.tile((0, 1, 2, 3, 4), 18)
    groups = np.row_stack((atr1, atr2))
    items = np.arange(0, GRP_SZ * NUM_GROUPS)
    group_info = np.row_stack((items, groups))
    intersectional = mf.make_intersectional_attribute(group_info, True)
    groups_inter = np.row_stack((items, intersectional))
    groups_info_with_inter = np.row_stack((group_info, intersectional))
    for i in range(0, len(levels)):
        base_ranks = np.genfromtxt(data_filenames[i], delimiter=',', dtype=int)

        for t in range(0,5):
            thresh_fairilp = thresh_fairilp_*(t+1)
            pthres = list(np.asarray(pthres_) * (t + 1))
            ithres = ithres_ * (t + 1)

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

            if method_type == "Fair_Kemeny":
                #optimization methods
                outputfile = "fair_kemeny_pof_delta_results.csv"

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
                gender_arp.append(ARP_a1)
                race_arp.append(ARP_a2)
                intersection_irp.append(irp_val)
                dataset.append(levels[i])
                theta_value.append(thetas[i])
                delta.append(ithres)
                pd_loss.append(mf.pd_loss(base_ranks, fair_soln))
                POF_pd.append(mf.POF_pd(base_ranks, kemeny_soln, fair_soln))

                # dictionary of lists
                dict = {'dataset': dataset, 'method': method, 'gender_arp': gender_arp, 'race_arp': race_arp,
                        'intersection_irp': intersection_irp, "theta_value": theta_value, "delta": delta,'pd_loss': pd_loss, 'POF_pd': POF_pd}

                results = pd.DataFrame(dict)
                print(results)
                results.to_csv(outputfile, index=False)

run_eval_pof_delta("Fair_Kemeny")


