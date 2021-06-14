"""
TO delete in repo
"""
import numpy as np
from multi_fair_ilp import *
from metrics import *
from utils import *
from vanilla_kemeny import *


ranks = np.array([[1, 2, 0, 3, 4, 5],
                   [1, 2, 0, 3, 4, 5],
                   [1, 2, 0, 3, 4, 5],
                   [2, 1, 0, 3, 4, 5]])

groups = np.array([[0, 1, 2, 3, 4, 5],
                   [0, 0, 1, 1, 2, 2]])

#Kemeny Agg
prob_result = aggregate_rankings(ranks)
Kemeny_soln = find_solution(prob_result, 6)
kemeny_objval = prob_result.objective.value()

#Fair Agg
prob_result = aggregate_rankings_fair_ilp(ranks, groups, [.05])
fair_soln = find_solution(prob_result, 6)
Fair_objval = prob_result.objective.value()

print("Kemeny Solution ", Kemeny_soln)
print("Kemeny obj val ", kemeny_objval)
print("Pairwise disagreement function Kemeny ", count_pairwise_disagreements(ranks, Kemeny_soln))
print("Fair Solution ", fair_soln)
print("Fair obj val ", Fair_objval)
print("Pairwise disagreement function Fair ", count_pairwise_disagreements(ranks, fair_soln))