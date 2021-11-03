"""
Script for Fair Schulze
"""
#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>

import numpy as np
from multi_fair.metrics import *
from multi_fair.utils import *
from multi_fair.correct_parity_policy import *
from multi_fair.ip import *
def fair_schulze(ranks, group_info, pthres, ithres):
    """   A function for finding the fair consensus ranking utilizing the schulze method
                :param ranks: A numpy array of base rankings, rows = rankings, col = candidates
                :param group_info: A numpy array of group_info[0] = candidate ids, and row vectors for each protected attribute's group labels
                :param pthres: A python list of protected attribute ARP thresholds
                :param ithres: An int of IRP threshold
                :return: A numpy array of the fair consensus ranking"""

    Qmat = all_pair_precedence(ranks)
    candidate_list = list(group_info[0,:])
    Pmat = np.zeros_like(Qmat)


    for i in candidate_list:
        for j in candidate_list:
            if i != j:
                if Qmat[j,i] > Qmat[i,j]:
                    Pmat[j,i] = Qmat[j,i]
                else:
                    Pmat[j,i] = 0

    for i in candidate_list:
        for j in candidate_list:
            if i != j:
                for k in candidate_list:
                    if i != k and j != k:
                        Pmat[k,j] = np.maximum(Pmat[k,j], np.minimum(Pmat[i,j],Pmat[k,i]))


    wins_candidate_has_over_others = np.sum(Pmat, axis = 0)
    zip_scores_items = zip(wins_candidate_has_over_others, candidate_list)
    sorted_pairs = sorted(zip_scores_items, reverse=True)
    schulze_ranking = [element for _, element in sorted_pairs]
    fair_consensus = correct_parity_policy(np.asarray(schulze_ranking), group_info, pthres, ithres, "both", True)
    return fair_consensus

