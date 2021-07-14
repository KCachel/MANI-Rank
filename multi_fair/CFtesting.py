"""
TO delete in repo
"""
import numpy as np
from multi_fair.multi_fair_ilp import *
from multi_fair.metrics import *
from multi_fair.utils import *
from multi_fair.vanilla_kemeny import *


##make diverging central ranking
NUM_GROUPS = 15
GRP_SZ = 6
atr1 = np.hstack((np.zeros(30, dtype=int), np.ones(30, dtype=int), np.ones(30, dtype=int) * 2))
atr2 = np.tile((0, 1, 2, 3, 4), 18)
groups = np.row_stack((atr1, atr2))
items = np.arange(0, GRP_SZ * NUM_GROUPS)
groups_key = np.row_stack((items, groups))
intersectional = make_intersectional_attribute(groups_key, True)
groups_inter = np.row_stack((items, intersectional))
groups_all_key = np.row_stack((groups_key, intersectional))
base_ranks = np.array([[25, 5, 10, 20, 15, 0, 70, 75, 80, 85, 60, 23, 24, 65, 2, 4, 69, 72, 8, 27, 3, 74, 77, 7, 68, 67, 78, 79, 9, 87, 13, 84, 14, 73, 17, 83, 22, 18, 28, 29, 19, 40, 82, 88, 16, 89, 6, 26, 50, 35, 30, 12, 21, 55, 62, 45, 64, 63, 1, 32, 34, 33, 37, 38, 76, 11, 39, 42, 43, 81, 71, 44, 47, 86, 48, 49, 52, 53, 54, 59, 57, 58, 61, 66, 31, 36, 41, 46, 51, 56]])

#prob_result = aggregate_rankings_fair_ilp(base_ranks, groups_key, [.3, .8, .6], True)
#soln = find_solution(prob_result, GRP_SZ * NUM_GROUPS)
soln = np.array([25, 70, 75, 80, 5, 85, 10, 15, 24, 4, 23, 67, 68, 69, 72, 73, 74, 77, 78, 79, 3, 82, 20, 2, 7, 83, 9, 84, 71, 8, 30, 76, 13, 27, 1, 87, 26, 45, 14, 88, 17, 40, 35, 50, 6, 81, 89, 18, 55, 19, 0, 16, 22, 28, 29, 32, 33, 86, 21, 34, 37, 60, 38, 39, 42, 31, 65, 43, 44, 47, 48, 49, 52, 53, 36, 54, 57, 41, 59, 58, 12, 46, 62, 63, 64, 51, 56, 11, 61, 66])
# attribute 1 parity
fpr_a1 = fpr(soln, np.row_stack((groups_key[0], groups_key[1])))
print(fpr_a1)
print("atr1 ARP ", rank_parity_score(fpr_a1))


# attribute 2 parity
fpr_a2 = fpr(soln, np.row_stack((groups_key[0], groups_key[2])))
print(fpr_a2)
print("atr2 ARP ", rank_parity_score(fpr_a2))

# intersectional parity
fpr_inter = fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[3])))
print(fpr_inter)
print("inter IRP ", rank_parity_score(fpr_inter))



ranks = np.array([[1, 2, 0, 3, 4, 5],
                   [1, 2, 0, 3, 4, 5],
                   [1, 2, 0, 3, 4, 5],
                   [2, 1, 0, 3, 4, 5]])

groups = np.array([[0, 1, 2, 3, 4, 5],
                   [0, 0, 1, 1, 2, 2]])

# #Kemeny Agg
# prob_result = aggregate_rankings(ranks)
# Kemeny_soln = find_solution(prob_result, 6)
# kemeny_objval = prob_result.objective.value()
#
# #Fair Agg
# prob_result = aggregate_rankings_fair_ilp(ranks, groups, [.05], False)
# fair_soln = find_solution(prob_result, 6)
# Fair_objval = prob_result.objective.value()
#
# print("Kemeny Solution ", Kemeny_soln)
# print("Kemeny obj val ", kemeny_objval)
# print("Pairwise disagreement function Kemeny ", count_pairwise_disagreements(ranks, Kemeny_soln))
# print("Fair Solution ", fair_soln)
# print("Fair obj val ", Fair_objval)
# print("Pairwise disagreement function Fair ", count_pairwise_disagreements(ranks, fair_soln))