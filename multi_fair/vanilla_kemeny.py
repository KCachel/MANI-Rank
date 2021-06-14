"""
Script for Kemeny Rank Aggregation (baseline) with no fairness constraints
"""

# Authors: Kathleen Cachel <kcachel@wpi.edu>
import numpy as np
import pulp as pl
from multi_fair.utils import *

path_to_cplex = r'/Applications/CPLEX_Studio201/cplex/bin/x86-64_osx/cplex'



ranks = np.array([[8, 5, 0, 2, 1, 9, 7, 3, 6, 4],
                  [1, 3, 2, 5, 9, 0, 4, 6, 7, 8],
                  [2, 4, 1, 9, 6, 8, 7, 0, 5, 3],
                  [9, 5, 0, 3, 7, 4, 6, 1, 8, 2],
                  [2, 8, 3, 6, 4, 5, 7, 9, 1, 0],
                  [2, 8, 6, 1, 9, 4, 5, 0, 3, 7],
                  [2, 5, 0, 4, 6, 9, 7, 8, 3, 1],
                  [6, 0, 4, 3, 2, 7, 8, 9, 5, 1]])
ranks_same = np.array([[8, 5, 0, 2, 1, 9, 7, 3, 6, 4],
                  [8, 5, 0, 2, 1, 9, 7, 3, 6, 4],
                  [8, 5, 0, 2, 1, 9, 7, 3, 6, 4],
                  [8, 5, 0, 2, 1, 9, 7, 3, 6, 4],
                  [8, 5, 0, 2, 1, 9, 7, 3, 6, 4],
                  [8, 5, 0, 2, 1, 9, 7, 3, 6, 4],
                  [8, 5, 0, 2, 1, 9, 7, 3, 6, 4],
                  [8, 5, 0, 2, 1, 9, 7, 3, 6, 4]])


groups = np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                   [0, 0, 0, 1, 1, 1, 1, 2, 2, 2],
                   [1, 0, 0, 1, 1, 0, 0, 0, 1, 1]])


def aggregate_rankings(ranks):
    n_voters, n_candidates = ranks.shape
    # construct
    pwin_cand = np.unique(ranks[0]).tolist()
    plose_cand = np.unique(ranks[0]).tolist()
    # convert pairwise wining/losing candidate index to string to index our variable
    plose_cand = [str(var) for var in plose_cand]
    pwin_cand = [str(var) for var in pwin_cand]
    cand = plose_cand


    # create a list of tuples containing all possible win row candidates and lose column candidates
    combos = [(i, j) for i in pwin_cand for j in plose_cand]

    #create a list of the precedence matrix representing the number of base rankings where a = row lost to b = col
    precedence_mat = all_pair_precedence(ranks)
    precedence_mat = precedence_mat.ravel()

    # create a dictionary to hold the weight for cand pair a and b, where cand a and cand b are keys and the #rankers put b above a is value (precedence mat)
    weight_dict = {}
    dur_iter = 0
    for (a, b) in combos:
        weight_dict[(a, b)] = precedence_mat[dur_iter]
        dur_iter = dur_iter + 1
    print(weight_dict)
    # Create the 'prob' variable to contain the problem data
    prob = pl.LpProblem("rank_agg", pl.LpMinimize)

    # Create the Xab variable
    X = pl.LpVariable.dicts("X", (pwin_cand, plose_cand), 0, 1, pl.LpInteger)

    # Add the objective function
    prob += pl.lpSum(X[a][b] * weight_dict[(a, b)] for (a,b) in combos)

    # The strict ordering constraint
    for (a, b) in combos:
        if a != b:
            prob += pl.lpSum(X[a][b] + X[b][a] ) == 1

    # The transitivity constraint
    for (a, b) in combos:
        if a != b:
            for c in cand:
                if c != a and c!= b:
                    prob += pl.lpSum(X[a][b] + X[b][c]+ X[c][a]) <= 2

    #prob.writeLP("rank_agg.lp")
    solver = pl.CPLEX_CMD(path=path_to_cplex, mip=True, options=['set mip tolerances integrality 0', 'set mip tolerances mipgap .005' ])
    prob.solve(solver)
    prob.roundSolution()
    print("Status:", pl.LpStatus[prob.status])

    # Print the variables
    for v in prob.variables():
        print(v.name, "=", v.varValue)

    return prob


