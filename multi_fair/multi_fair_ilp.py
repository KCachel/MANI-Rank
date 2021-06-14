"""
Script for Multi-Fair ILP
"""
# Authors: Kathleen Cachel <kcachel@wpi.edu>

import numpy as np
import pulp as pl
from itertools import combinations
from multi_fair.utils import *
path_to_cplex = r'/Applications/CPLEX_Studio201/cplex/bin/x86-64_osx/cplex'




def generate_mixed_pairs_per_item(attribute_dict, n_candidates):
    mpair_dict = {}
    keys_list = list(attribute_dict) #in order to index attribute_dict
    for aval in range(len(attribute_dict)):
        items = attribute_dict[keys_list[aval]]
        mpair_cnt = len(items)*(n_candidates - len(items))
        for it in items:
            mpair_dict[it] = mpair_cnt
    return mpair_dict


def aggregate_rankings_fair_ilp(ranks, groups, thres_vals):
    global attribute_dict
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

    # create a list of the precedence matrix representing the number of base rankings where a = row lost to b = col
    precedence_mat = all_pair_precedence(ranks)
    precedence_mat = precedence_mat.ravel()

    # create a dictionary to hold the weight for cand pair a and b, where cand a and cand b are keys and the #rankers put b above a is value (precedence mat)
    weight_dict = {}
    dur_iter = 0
    for (a, b) in combos:
        weight_dict[(a, b)] = precedence_mat[dur_iter]
        dur_iter = dur_iter + 1
    #print(weight_dict)
    # Create the 'prob' variable to contain the problem data
    prob = pl.LpProblem("rank_agg", pl.LpMinimize)

    # Create the Xab variable
    #X = pl.LpVariable.dicts("X", (pwin_cand, plose_cand), 0, 1, pl.LpInteger)
    X = pl.LpVariable.dicts("X", (pwin_cand, plose_cand), 0, 1, cat= 'Integer')
    # Add the objective function
    prob += pl.lpSum(X[a][b] * weight_dict[(a, b)] for (a,b) in combos)

    # The strict ordering constraint
    for (a, b) in combos:
        if a != b:
            prob += pl.lpSum(X[a][b] + X[b][a]) == 1

    # The transitivity constraint
    for (a, b) in combos:
        if a != b:
            for c in cand:
                if c != a and c != b:
                    prob += pl.lpSum(X[a][b] + X[b][c] + X[c][a]) <= 2

    # Group Parity
    num_attributes = groups.shape[0] - 1

    for atr in range(0, num_attributes):

        thres = thres_vals[atr]
        atr = atr + 1
        attribute_dict = determine_group_identity(groups[0], groups[atr])
        mpair_dict = generate_mixed_pairs_per_item(attribute_dict, n_candidates)
        # in order to index dictionary
        keys_list = list(attribute_dict)

        #binary case
        if len(attribute_dict) == 2:
            mixed_pairs = [(i, j) for i in attribute_dict[keys_list[0]] for j in attribute_dict[keys_list[1]]]
            # add constraint
            prob += pl.lpSum(((1/mpair_dict[a])*X[a][b] - (1/mpair_dict[b])*X[b][a]) for (a, b) in mixed_pairs) <= thres
            prob += pl.lpSum((-(1/mpair_dict[a])*X[a][b] + (1/mpair_dict[b])*X[b][a]) for (a, b) in mixed_pairs) <= thres
        #multiclass case
        if len(attribute_dict) > 2:
            #get all size 2 combination of the groups
            combos = list(combinations(list(np.unique(groups[atr])), 2))
            for combo in combos:
                # get !cur_grp vals
                keys = [item for item in np.unique(groups[atr])] #key = group label
                groupa = [attribute_dict.get(key) for key in keys if key == combo[0]] #first group in combo
                not_groupa = [attribute_dict.get(key) for key in keys if key != combo[0]] #not first group in combo
                groupb = [attribute_dict.get(key) for key in keys if key == combo[1]] #second group in combo
                not_groupb = [attribute_dict.get(key) for key in keys if key != combo[1]]  # not second group in combo
                # flatten the lists of list
                groupa = [y for x in groupa for y in x]
                not_groupa = [y for x in not_groupa for y in x]
                groupb = [y for x in groupb for y in x]
                not_groupb = [y for x in not_groupb for y in x]
                # create mixed pairs of cur_group and other_grps
                groupa_pairs = [(i, j) for i in groupa for j in not_groupa]
                groupb_pairs = [(i, j) for i in groupb for j in not_groupb]
                print("mpair_dict ", mpair_dict)

                # add constraint
                prob += (pl.lpSum((1/mpair_dict[a])*X[a][b] for (a, b) in groupa_pairs) - pl.lpSum(
                    (1/mpair_dict[c])*X[c][d] for (c,d) in groupb_pairs)) <= thres
                prob += (pl.lpSum(-(1 / mpair_dict[a]) * X[a][b] for (a, b) in groupa_pairs) + pl.lpSum(
                    (1 / mpair_dict[c]) * X[c][d] for (c, d) in groupb_pairs)) <= thres


    #prob.writeLP("rank_agg_fairilpmulti.lp")

    solver = pl.CPLEX_CMD(path = path_to_cplex, mip = True, options=['set mip tolerances integrality 0', 'set mip tolerances mipgap .005' ])
    prob.solve(solver)
    prob.roundSolution()
    print("Status:", pl.LpStatus[prob.status])
    #
    # Print the variables
    for v in prob.variables():
        print(v.name, "=", v.varValue)

    return prob


