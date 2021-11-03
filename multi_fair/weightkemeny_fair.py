"""
Script for Kemeny-Weighted
"""
#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>

import numpy as np
from multi_fair.metrics import *
from multi_fair.utils import *
from multi_fair.correct_parity_policy import *
from multi_fair.ip import *
from multi_fair.vanilla_kemeny import *
path_to_cplex = r'C:\Program Files\IBM\ILOG\CPLEX_Studio201\cplex\bin\x64_win64\cplex.exe'

def weight_kemeny_fair(ranks, group_info, pthres, ithres, inter_given):
    """   A function for finding the fair consensus ranking utilizing the copeland method
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
    avg_fairness = []
    for rank_i in range(0, num_rankings):
        ranking = ranks[rank_i,:]
        scores = []
        for pa_i in range(0,num_patr):
            fpr_ = fpr(ranking, np.row_stack((group_info[0], group_info[pa_i])))
            scores.append(rank_parity_score(fpr_))

        # intersectional parity
        fpr_inter = fpr(ranking, np.row_stack((group_info[0], group_info[-1])))
        scores.append(rank_parity_score(fpr_inter))

        avg_fairness.append(np.mean(scores))
    s = np.array(avg_fairness)
    sort_index = np.argsort(-s)


    base_ranks = ranks[sort_index[0], :]
    for i in range(1,len(sort_index)):
        rank_i = sort_index[i]
        ranking = ranks[rank_i,:]
        base_ranks = np.vstack((base_ranks,ranking))


    prob_result = aggregate_rankings_weight(ranks)
    fair_soln = find_solution(prob_result, num_candidates)

    return fair_soln





def aggregate_rankings_weight(ranks):
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
    precedence_mat = all_pair_precedence_weight(ranks)
    precedence_mat = precedence_mat.ravel()

    # create a dictionary to hold the weight for cand pair a and b, where cand a and cand b are keys and the #rankers put b above a is value (precedence mat)
    weight_dict = {}
    dur_iter = 0
    for (a, b) in combos:
        weight_dict[(a, b)] = precedence_mat[dur_iter]
        dur_iter = dur_iter + 1

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
    solver = pl.CPLEX_CMD(path=path_to_cplex, mip=True, options=['set mip tolerances integrality 0'])
    prob.solve(solver)
    prob.roundSolution()
    print("Status:", pl.LpStatus[prob.status])


    return prob