"""
Script for Fair_Borda
"""
#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>

import numpy as np
from multi_fair.metrics import *
from multi_fair.utils import *


def fair_borda(ranks, group_info, pthres, ithres):
    """   A function for finding a fair consensus ranking with Borda
                :param ranks: A numpy array of base rankings, rows = rankings, col = candidates
                :param group_info: A numpy array of group_info[0] = candidate ids, and row vectors for each protected attribute's group labels
                :param pthres: A python list of protected attribute ARP thresholds
                :param ithres: An int of IRP threshold
                :return: A numpy array of the fair consensus ranking"""
    item_list = list(np.unique(ranks[0, :]))
    bordaDict = {key: 0 for key in item_list}
    num_rankings, num_items = ranks.shape
    points_per_pos_legend = list(range(num_items -1 , -1, -1))

    for ranking in range(0, num_rankings):
        for item_pos in range(0, num_items):
            item = ranks[ranking, item_pos]
            bordaDict[item] += points_per_pos_legend[item_pos]

    candidates = list(bordaDict.keys())
    borda_scores = list(bordaDict.values())
    zip_scores_items = zip(borda_scores, candidates)
    sorted_pairs = sorted(zip_scores_items, reverse=True)
    borda_ranking = [element for _, element in sorted_pairs]
    fair_consensus = correct_parity_policy(np.asarray(borda_ranking), group_info, pthres, ithres, "both", True)
    return fair_consensus


