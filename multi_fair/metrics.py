"""Metrics for assessing statistical parity, and allocation of positive outcome
"""
# Authors: Kathleen Cachel <kcachel@wpi.edu>
import numpy as np
from multi_fair.utils import *

ranking = np.array([0, 3, 4, 5, 6, 1, 2])
group_key = np.array([[0, 1, 2, 3, 4, 5, 6],
                      [0, 1, 0, 1, 2, 3, 2]])



def fpr(ranking, group_key):
    """   Compute the Favored Pair Representation of each group in the encoded attribute.
                    :param ranking: A numpy array of ranking over the candidates
                    :param group_key: A numpy array first row is candidates ids, second row is identity for protected attribute
                    :return fpr: python list of fpr score for each group (indexed by group id)"""
    candidates = group_key[0]
    grp_mem = group_key[1]
    num_groups = len(np.unique(grp_mem))
    r_list = list(ranking)
    groups_of_candidates = candidates_by_group(candidates, grp_mem)
    fpr = []
    pair_cnt = pair_count_at_position_array(len(ranking))
    pairs_in_ranking = pair_count(len(ranking))

    for i in range(0,num_groups):
        cands = groups_of_candidates[i]
        grp_sz = len(cands)
        total_favored = 0
        for x in cands:
            indx_in_r = r_list.index(x)
            favored_pairs_at_pos = pair_cnt[indx_in_r]
            total_favored += favored_pairs_at_pos
        #numerator
        favored_over_other_grp = total_favored - pair_count(grp_sz)
        #denominator
        total_mixed_with_group = grp_sz*(len(ranking) - grp_sz)
        fpr.append(favored_over_other_grp/total_mixed_with_group)
    return fpr


def rank_parity_score(fpr):
    """   Compute the Attribute or Intersectional Rank Parity.
                    :param fpr: A python list of fpr scores
                    :return RP: float attribute or intersectional rank parity"""
    max_value = np.max(np.asarray(fpr))
    min_value = np.min(np.asarray(fpr))
    RP = max_value - min_value
    return RP

def cost_fairness(base_rankings, kemeny_ranking, fair_ranking):
    kemeny_obj = count_pairwise_disagreements(base_rankings, kemeny_ranking)
    fair_obj = count_pairwise_disagreements(base_rankings, fair_ranking)
    return kemeny_obj - fair_obj




