"""
Script for Student Case Study
"""

# License: GNU GENERAL PUBLIC LICENSE
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


def run_exam_case_study():
    ranks_file = 'exam_base_rankings.csv'
    group_info_file = 'exam_group_key.csv'
    outputfile = 'exam_results.csv'
    base_ranks = np.genfromtxt(ranks_file, delimiter=',', dtype=int).T  # transpose to be of ranks x candidates

    group_info = np.genfromtxt(group_info_file, delimiter=',', dtype=int).T  # transpose to be of groups x candidates
    intersectional = mf.make_intersectional_attribute(group_info, True)
    groups_info_with_inter = np.row_stack((group_info, intersectional))

    pthres = [.05, .05, .05]
    ithres = .05
    thresh_fairilp = [.05, .05, .05, .05]

    method = []
    fpr_gender = []
    fpr_race = []
    fpr_lunch = []
    arp_gender = []
    arp_race = []
    arp_lunch = []
    fpr_inter = []
    IRP = []

    ranks = ['math', 'reading', 'writing']

    for r in range(len(ranks)):
        rank = base_ranks[r, :]

        fpr_gender_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
        fpr_gender.append(fpr_gender_)
        arp_gender.append(mf.rank_parity_score(fpr_gender_))

        fpr_race_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
        fpr_race.append(fpr_race_)
        arp_race.append(mf.rank_parity_score(fpr_race_))

        fpr_lunch_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[3])))
        fpr_lunch.append(fpr_lunch_)
        arp_lunch.append(mf.rank_parity_score(fpr_lunch_))

        fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[4])))
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

    fpr_gender_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_gender.append(fpr_gender_)
    arp_gender.append(mf.rank_parity_score(fpr_gender_))

    fpr_race_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_race.append(fpr_race_)
    arp_race.append(mf.rank_parity_score(fpr_race_))

    fpr_lunch_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[3])))
    fpr_lunch.append(fpr_lunch_)
    arp_lunch.append(mf.rank_parity_score(fpr_lunch_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[4])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Kemeny")


    # WEIGHTED KEMENY
    rank = mf.weight_kemeny_fair(base_ranks, groups_info_with_inter, pthres, ithres, True)

    print("weighted kemeny")

    fpr_gender_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_gender.append(fpr_gender_)
    arp_gender.append(mf.rank_parity_score(fpr_gender_))

    fpr_race_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_race.append(fpr_race_)
    arp_race.append(mf.rank_parity_score(fpr_race_))

    fpr_lunch_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[3])))
    fpr_lunch.append(fpr_lunch_)
    arp_lunch.append(mf.rank_parity_score(fpr_lunch_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[4])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))

    method.append("Weighted_Kemeny")


    # FAIR ILP

    prob_result = mf.aggregate_rankings_fair_ilp(base_ranks, groups_info_with_inter, thresh_fairilp, True)
    rank = mf.find_solution(prob_result, base_ranks.shape[1])

    print("fair ilp")

    fpr_gender_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_gender.append(fpr_gender_)
    arp_gender.append(mf.rank_parity_score(fpr_gender_))

    fpr_race_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_race.append(fpr_race_)
    arp_race.append(mf.rank_parity_score(fpr_race_))

    fpr_lunch_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[3])))
    fpr_lunch.append(fpr_lunch_)
    arp_lunch.append(mf.rank_parity_score(fpr_lunch_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[4])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Fair_Kemeny")




    # FAIR SCHULZE

    rank = mf.fair_schulze(base_ranks, groups_info_with_inter, pthres, ithres)

    print("schulze")

    fpr_gender_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_gender.append(fpr_gender_)
    arp_gender.append(mf.rank_parity_score(fpr_gender_))

    fpr_race_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_race.append(fpr_race_)
    arp_race.append(mf.rank_parity_score(fpr_race_))

    fpr_lunch_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[3])))
    fpr_lunch.append(fpr_lunch_)
    arp_lunch.append(mf.rank_parity_score(fpr_lunch_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[4])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Fair_Schulze")



    # FAIR BORDA

    rank = mf.fair_borda(base_ranks, groups_info_with_inter, pthres, ithres)
    print("borda")

    fpr_gender_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_gender.append(fpr_gender_)
    arp_gender.append(mf.rank_parity_score(fpr_gender_))

    fpr_race_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_race.append(fpr_race_)
    arp_race.append(mf.rank_parity_score(fpr_race_))

    fpr_lunch_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[3])))
    fpr_lunch.append(fpr_lunch_)
    arp_lunch.append(mf.rank_parity_score(fpr_lunch_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[4])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Fair_Borda")


    # FAIR COPELAND

    rank = mf.fair_copeland(base_ranks, groups_info_with_inter, pthres, ithres)

    print("COPELAND")

    fpr_gender_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_gender.append(fpr_gender_)
    arp_gender.append(mf.rank_parity_score(fpr_gender_))

    fpr_race_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_race.append(fpr_race_)
    arp_race.append(mf.rank_parity_score(fpr_race_))

    fpr_lunch_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[3])))
    fpr_lunch.append(fpr_lunch_)
    arp_lunch.append(mf.rank_parity_score(fpr_lunch_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[4])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Fair_Copeland")

    # PICK FAIREST PERM

    rank = mf.pick_fairest_perm(base_ranks, groups_info_with_inter, pthres, ithres, True)

    print("pick fairest perm")

    fpr_gender_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_gender.append(fpr_gender_)
    arp_gender.append(mf.rank_parity_score(fpr_gender_))

    fpr_race_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_race.append(fpr_race_)
    arp_race.append(mf.rank_parity_score(fpr_race_))

    fpr_lunch_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[3])))
    fpr_lunch.append(fpr_lunch_)
    arp_lunch.append(mf.rank_parity_score(fpr_lunch_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[4])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Pick_Fairest_Perm")

    # CORRECT FAIREST PERM

    rank = mf.correct_fairest_perm(base_ranks, groups_info_with_inter, pthres, ithres, True)

    print("correct fairest perm")

    fpr_gender_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[1])))
    fpr_gender.append(fpr_gender_)
    arp_gender.append(mf.rank_parity_score(fpr_gender_))

    fpr_race_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[2])))
    fpr_race.append(fpr_race_)
    arp_race.append(mf.rank_parity_score(fpr_race_))

    fpr_lunch_ = mf.fpr(rank, np.row_stack((group_info[0], group_info[3])))
    fpr_lunch.append(fpr_lunch_)
    arp_lunch.append(mf.rank_parity_score(fpr_lunch_))

    fpr_inter_ = mf.fpr(rank, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[4])))
    fpr_inter.append(fpr_inter_)
    IRP.append(mf.rank_parity_score(fpr_inter_))
    method.append("Correct_Fairest_Perm")

    # dictionary of lists
    dict = {'method': method, 'fpr_lunch': fpr_lunch, 'arp_lunch': arp_lunch,
            'fpr_gender': fpr_gender, 'fpr_race': fpr_race, 'arp_gender': arp_gender,
            'arp_race': arp_race, 'fpr_inter': fpr_inter, 'IRP': IRP}

    results = pd.DataFrame(dict)
    print(results)
    results.to_csv(outputfile, index=False)


run_exam_case_study()
