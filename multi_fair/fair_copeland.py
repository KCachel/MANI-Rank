"""
Script for Fair-Copeland
"""
#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>

import numpy as np
from multi_fair.metrics import *
from multi_fair.utils import *
from multi_fair.correct_parity_policy import *
from multi_fair.ip import *
def fair_copeland(ranks, group_info, pthres, ithres):
    """   A function for finding the fair consensus ranking utilizing the copeland method
                :param ranks: A numpy array of base rankings, rows = rankings, col = candidates
                :param group_info: A numpy array of group_info[0] = candidate ids, and row vectors for each protected attribute's group labels
                :param pthres: A python list of protected attribute ARP thresholds
                :param ithres: An int of IRP threshold
                :return: A numpy array of the fair consensus ranking"""
    item_list = list(np.unique(ranks[0, :]))
    copelandDict = {key: 0 for key in item_list}
    num_rankings, num_items = ranks.shape
    Qmat = all_pair_precedence(ranks)
    candidate_list = list(group_info[0, :])

    for item in candidate_list:
        for comparison_item in candidate_list:
            if item != comparison_item:
                num_item_wins = Qmat[comparison_item, item]
                num_comparison_item_wins = Qmat[item, comparison_item]
                if num_item_wins >= num_comparison_item_wins:
                    copelandDict[item] += 1

    candidates = list(copelandDict.keys())
    copeland_pairwon_cnt = list(copelandDict.values())
    zip_scores_items = zip(copeland_pairwon_cnt, candidates)
    sorted_pairs = sorted(zip_scores_items, reverse=True)
    copeland_ranking = [element for _, element in sorted_pairs]
    fair_consensus = correct_parity_policy(np.asarray(copeland_ranking), group_info, pthres, ithres, "both", True)
    return fair_consensus



