"""
Script for CSRankings Case Study
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

def run_cs_case_study( ):

    outputfile = 'csranks_results.csv'
    base_ranks = np.load('cs_baseranks.npy').astype(int)
    group_info_file = 'cs_groups.csv'

    group_info = np.genfromtxt(group_info_file, delimiter=',',
                               dtype=int).T  # transpose to be of attributes x candidates

    intersectional = mf.make_intersectional_attribute(group_info, True)
    groups_info_with_inter = np.row_stack((group_info, intersectional))


    pthres = [.1, .1]
    ithres = .1
    thresh_fairilp = [.1, .1, .1]


    method = []
    fpr_location = []
    fpr_type = []
    arp_location = []
    arp_type = []
    fpr_inter = []
    IRP = []

    ranks = list(map(str, range(2000, 2021, 1) ))

    for r in range(len(ranks)):
        rank = base_ranks[r, :]

        fpr_location_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
        fpr_location.append(fpr_location_)
        arp_location.append(mf.rank_parity_score(fpr_location_))

        fpr_type_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
        fpr_type.append(fpr_type_)
        arp_type.append(mf.rank_parity_score(fpr_type_))

        fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
        fpr_inter.append(fpr_inter_)
        IRP.append(mf.rank_parity_score(fpr_inter_))

        method.append(ranks[r])


    #####################
    # METHODS
    #####################



    # KEMENY
    prob_result = mf.aggregate_rankings(base_ranks)
    rank = mf.find_solution(prob_result, base_ranks.shape[1])


    print("kemeny")

    fpr_location_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_location.append(fpr_location_)
    arp_location.append(mf.rank_parity_score(fpr_location_))

    fpr_type_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_type.append(fpr_type_)
    arp_type.append(mf.rank_parity_score(fpr_type_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Kemeny")


    # WEIGHTED KEMENY
    rank = mf.weight_kemeny_fair(base_ranks, groups_info_with_inter, pthres, ithres, True)

    print("weighted kemeny")

    fpr_location_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_location.append(fpr_location_)
    arp_location.append(mf.rank_parity_score(fpr_location_))

    fpr_type_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_type.append(fpr_type_)
    arp_type.append(mf.rank_parity_score(fpr_type_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))

    method.append("Weighted_Kemeny")


    # FAIR ILP

    prob_result = mf.aggregate_rankings_fair_ilp(base_ranks, groups_info_with_inter, thresh_fairilp, True)
    rank = mf.find_solution(prob_result, base_ranks.shape[1])

    print("fair ilp")

    fpr_location_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_location.append(fpr_location_)
    arp_location.append(mf.rank_parity_score(fpr_location_))

    fpr_type_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_type.append(fpr_type_)
    arp_type.append(mf.rank_parity_score(fpr_type_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Fair_Kemeny")




    # FAIR SCHULZE

    rank = mf.fair_schulze(base_ranks, groups_info_with_inter, pthres, ithres)

    print("schulze")

    fpr_location_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_location.append(fpr_location_)
    arp_location.append(mf.rank_parity_score(fpr_location_))

    fpr_type_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_type.append(fpr_type_)
    arp_type.append(mf.rank_parity_score(fpr_type_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Fair_Schulze")



    # FAIR BORDA

    rank = mf.fair_borda(base_ranks, groups_info_with_inter, pthres, ithres)
    print("borda")

    fpr_location_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_location.append(fpr_location_)
    arp_location.append(mf.rank_parity_score(fpr_location_))

    fpr_type_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_type.append(fpr_type_)
    arp_type.append(mf.rank_parity_score(fpr_type_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Fair_Borda")


    # FAIR COPELAND

    rank = mf.fair_copeland(base_ranks, groups_info_with_inter, pthres, ithres)

    print("COPELAND")

    fpr_location_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_location.append(fpr_location_)
    arp_location.append(mf.rank_parity_score(fpr_location_))

    fpr_type_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_type.append(fpr_type_)
    arp_type.append(mf.rank_parity_score(fpr_type_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Fair_Copeland")

    # PICK FAIREST PERM

    rank = mf.pick_fairest_perm(base_ranks, groups_info_with_inter, pthres, ithres, True)

    print("pick fairest perm")

    fpr_location_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_location.append(fpr_location_)
    arp_location.append(mf.rank_parity_score(fpr_location_))

    fpr_type_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_type.append(fpr_type_)
    arp_type.append(mf.rank_parity_score(fpr_type_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Pick_Fairest_Perm")

    # CORRECT FAIREST PERM

    rank = mf.correct_fairest_perm(base_ranks, groups_info_with_inter, pthres, ithres, True)

    print("correct fairest perm")

    fpr_location_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_location.append(fpr_location_)
    arp_location.append(mf.rank_parity_score(fpr_location_))

    fpr_type_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_type.append(fpr_type_)
    arp_type.append(mf.rank_parity_score(fpr_type_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Correct_Fairest_Perm")


    # dictionary of lists
    dict = {'method': method, 'fpr_location': fpr_location, 'arp_location': arp_location,
            'fpr_type': fpr_type, 'arp_type': arp_type,'fpr_inter': fpr_inter, 'IRP': IRP}


    results = pd.DataFrame(dict)
    print(results)
    results.to_csv(outputfile, index=False)


run_cs_case_study()