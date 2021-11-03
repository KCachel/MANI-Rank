
"""
Script for Correct-Fairest-Perm
"""
#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>

import numpy as np
from multi_fair.metrics import *
from multi_fair.utils import *
from multi_fair.correct_parity_policy import *
from multi_fair.ip import *
def correct_fairest_perm(ranks, group_info, pthres, ithres,inter_given):
    """   A function for finding the fair consensus 
                :param ranks: A numpy array of base rankings, rows = rankings, col = candidates
                :param group_info: A numpy array of group_info[0] = candidate ids, and row vectors for each protected attribute's group labels
                :param pthres: A python list of protected attribute ARP thresholds
                :param ithres: An int of IRP threshold
                :return: A numpy array of the fair consensus ranking"""
    num_rankings, num_candidates = ranks.shape
    num_patr = group_info.shape[0] - 1
    if not inter_given:  # False, then make it
        intersectional = make_intersectional_attribute(group_info, False)
        group_info = np.row_stack((group_info, intersectional))
    best_avg_score = 0
    best_ranking_ind = 0
    for rank_i in range(0, num_rankings):
        ranking = ranks[rank_i,:]
        scores = []
        for pa_i in range(0,num_patr):
            fpr_ = fpr(ranking, np.row_stack((group_info[0], group_info[pa_i])))
            scores.append(rank_parity_score(fpr_))

        # intersectional parity
        fpr_inter = fpr(ranking, np.row_stack((group_info[0], group_info[-1])))
        scores.append(rank_parity_score(fpr_inter))

        if np.mean(scores) > best_avg_score:
            best_ranking_ind = rank_i

    best_ranking = ranks[best_ranking_ind,:]
    fair_consensus = correct_parity_policy(best_ranking, group_info, pthres, ithres, "both", True)

    return fair_consensus

