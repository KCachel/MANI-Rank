"""Metrics for assessing statistical parity, POF, PD_loss, and allocation of positive outcome
"""

#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>
import numpy as np
from multi_fair.utils import *


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
        total_favored = int(0)
        for x in cands:
            indx_in_r = r_list.index(x)
            favored_pairs_at_pos = pair_cnt[indx_in_r]
            total_favored += int(favored_pairs_at_pos)
        #numerator
        favored_over_other_grp = total_favored - pair_count(grp_sz)
        #print("numerator in parity : ",favored_over_other_grp)
        #denominator
        total_mixed_with_group = grp_sz*(len(ranking) - grp_sz)
        fpr.append(favored_over_other_grp/total_mixed_with_group)
        #print("denominator in parity: ", total_mixed_with_group)
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
    return fair_obj - kemeny_obj

def pd_loss(base_rankings, ranking):
    n_voters, n_candidates = base_rankings.shape
    pairwise_disagreements = count_pairwise_disagreements(base_rankings, ranking)
    pd_loss = pairwise_disagreements/(pair_count(n_candidates)*n_voters)
    return pd_loss

def POF_pd(base_rankings, kemeny_ranking, fair_ranking):
    pd_loss_kem = pd_loss(base_rankings, kemeny_ranking)
    pd_loss_fair = pd_loss(base_rankings, fair_ranking)
    return pd_loss_fair - pd_loss_kem



