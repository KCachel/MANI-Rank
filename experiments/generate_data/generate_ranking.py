

import numpy as np
import pulp as pl
from itertools import combinations, permutations
from collections import Counter
from more_itertools import unique_everseen
import multi_fair as mf
path_to_cplex = r'/Applications/CPLEX_Studio201/cplex/bin/x86-64_osx/cplex'

def ranking_with_group_labels(ranking, candidates, group_labels):

    ranking_group_labels = []
    for cand in range(0,len(ranking)):
        ranking_group_labels.append(group_labels[np.where(candidates == ranking[cand])[0][0]])
    return ranking_group_labels


def find_solution(prob, num_candidates):
    #collect variables that are true
    true_vars = [v.name for v in prob.variables() if v.varValue == 1]
    top_of_pair_candidate = [var.split('_')[1] for var in true_vars]
    # sorting on basis of frequency of elements
    result = [item for items, c in Counter(top_of_pair_candidate).most_common()
              for item in [items] * c]
    #get unique elements while preserving order
    solution = list(unique_everseen(result))
    #convert string candidates to ints
    solution = list(map(int, solution))
    #append last candidate
    bottom_candidate = [item for item in range(0,num_candidates) if item not in solution]
    solution.append(bottom_candidate[0])
    return solution

def determine_group_identity(candidates, grp_mem):
    group_id_dict = {}
    for var in np.unique(grp_mem):
        idx = np.where(grp_mem == var)
        group_id_dict[(var)] = [str(item) for item in candidates[idx].tolist()]  # make it a list of str
    return group_id_dict

def generate_mixed_pairs_per_item(attribute_dict, n_candidates):
    mpair_dict = {}
    keys_list = list(attribute_dict) #in order to index attribute_dict
    for aval in range(len(attribute_dict)):
        items = attribute_dict[keys_list[aval]]
        mpair_cnt = len(items)*(n_candidates - len(items))
        for it in items:
            mpair_dict[it] = mpair_cnt
    return mpair_dict


def generate_ranking(groups, lower, upper):
    intersectional = mf.make_intersectional_attribute(groups, True)
    groups = np.row_stack((groups, intersectional))
    global attribute_dict
    _,n_candidates = groups.shape
    # construct
    pwin_cand = np.unique(groups[0]).tolist()
    plose_cand = np.unique(groups[0]).tolist()
    # convert pairwise wining/losing candidate index to string to index our variable
    plose_cand = [str(var) for var in plose_cand]
    pwin_cand = [str(var) for var in pwin_cand]
    cand = plose_cand

    # create a list of tuples containing all possible win row candidates and lose column candidates
    combos = [(i, j) for i in pwin_cand for j in plose_cand]

    # Create the 'prob' variable to contain the problem data
    prob = pl.LpProblem("generate_ilp", pl.LpMinimize)

    # Create the Xab variable
    X = pl.LpVariable.dicts("X", (pwin_cand, plose_cand), 0, 1, cat= 'Integer')
    # Add the objective function
    #prob += pl.lpSum(X[a][b] for (a,b) in combos)
    prob += pl.lpSum(0)

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
    num_attributes = len(lower)

    for atr in range(0, num_attributes):

        l_thres = lower[atr]
        u_thres = upper[atr]
        atr = atr + 1
        attribute_dict = determine_group_identity(groups[0], groups[atr])
        mpair_dict = generate_mixed_pairs_per_item(attribute_dict, n_candidates)
        # in order to index dictionary
        keys_list = list(attribute_dict)

        #binary case
        if len(attribute_dict) == 2:
            mixed_pairs = [(i, j) for i in attribute_dict[keys_list[0]] for j in attribute_dict[keys_list[1]]]
            # add constraint
            prob += pl.lpSum(((1/mpair_dict[a])*X[a][b] - (1/mpair_dict[b])*X[b][a]) for (a, b) in mixed_pairs) <= u_thres
            prob += pl.lpSum(
                ((1 / mpair_dict[a]) * X[a][b] - (1 / mpair_dict[b]) * X[b][a]) for (a, b) in mixed_pairs) >= l_thres
            #prob += pl.lpSum((-(1/mpair_dict[a])*X[a][b] + (1/mpair_dict[b])*X[b][a]) for (a, b) in mixed_pairs) == thres
        #multiclass case
        if len(attribute_dict) > 2:
            #get all size 2 combination of the groups
            combos = list(combinations(list(np.unique(groups[atr])), 2))
            cnt = 0 #so that first constraint is equality
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


                # add constraint
                if cnt > 0:
                    prob += (pl.lpSum((1/mpair_dict[a])*X[a][b] for (a, b) in groupa_pairs) - pl.lpSum(
                        (1/mpair_dict[c])*X[c][d] for (c,d) in groupb_pairs)) <= l_thres
                    prob += (pl.lpSum(-(1 / mpair_dict[a]) * X[a][b] for (a, b) in groupa_pairs) + pl.lpSum(
                        (1 / mpair_dict[c]) * X[c][d] for (c, d) in groupb_pairs)) <= l_thres
                else:
                    prob += (pl.lpSum((1 / mpair_dict[a]) * X[a][b] for (a, b) in groupa_pairs) - pl.lpSum(
                        (1 / mpair_dict[c]) * X[c][d] for (c, d) in groupb_pairs)) <= u_thres
                    prob += (pl.lpSum((1 / mpair_dict[a]) * X[a][b] for (a, b) in groupa_pairs) - pl.lpSum(
                        (1 / mpair_dict[c]) * X[c][d] for (c, d) in groupb_pairs)) >= l_thres
                    # prob += (pl.lpSum(-(1 / mpair_dict[a]) * X[a][b] for (a, b) in groupa_pairs) + pl.lpSum(
                    #     (1 / mpair_dict[c]) * X[c][d] for (c, d) in groupb_pairs)) == thres
                    cnt += 1



    prob.writeLP("generate_ilp.lp")

    solver = pl.CPLEX_CMD(path = path_to_cplex, mip = True, options=['set mip tolerances integrality 0', 'set mip tolerances mipgap .1'])
    prob.solve(solver)
    prob.roundSolution()
    print("Status:", pl.LpStatus[prob.status])
    #
    # Print the variables
    for v in prob.variables():
        print(v.name, "=", v.varValue)
        #print("type", type(v.varValue))
    return prob, groups



NUM_GROUPS = 15
GRP_SZ = 6
atr1 = np.hstack((np.zeros(30, dtype=int), np.ones(30, dtype=int),np.ones(30, dtype=int)*2))
atr2 = np.tile((0, 1, 2, 3, 4), 18)
atr3 = np.tile((0,1), 45)
atr4 = np.hstack((np.zeros(30, dtype=int), np.ones(30, dtype=int),np.ones(30, dtype=int)*2))
groups = np.row_stack((atr1, atr2, atr3))
items = np.arange(0, GRP_SZ*NUM_GROUPS)

groups = np.row_stack((items, groups))
intersectional = mf.make_intersectional_attribute(groups, True)
groups_inter = np.row_stack((items, intersectional, atr2))
groups_all_key = np.row_stack((groups, intersectional))

prob_result, groups_calc = generate_ranking(groups_inter, [.3, .3], [.4, .9])
soln = find_solution(prob_result, GRP_SZ*NUM_GROUPS)

print("solution ", soln)
#groups_for_atr1 = ranking_with_group_labels(soln, groups[0], groups[1])
fpr_a1 = mf.fpr(soln, np.row_stack((groups[0], groups[1])))
print("FPR ", fpr_a1)
print("ARP ", mf.rank_parity_score(fpr_a1))

#groups_for_atr2 = ranking_with_group_labels(soln, groups[0], groups[2])
fpr_a2 = mf.fpr(soln, np.row_stack((groups[0], groups[2])))
print("FPR ", fpr_a2)
print("ARP ", mf.rank_parity_score(fpr_a2))

fpr_a3 = mf.fpr(soln, np.row_stack((groups[0], groups[3])))
print("FPR ", fpr_a3)
print("ARP ", mf.rank_parity_score(fpr_a3))

# fpr_a4 = mf.fpr(soln, np.row_stack((groups[0], groups[4])))
# print("FPR ", fpr_a4)
# print("ARP ", mf.rank_parity_score(fpr_a4))


fpr_intersectional = mf.fpr(soln,np.row_stack((groups[0], groups_all_key[4])))
print("FPR ", fpr_intersectional)
print("IRP ", mf.rank_parity_score(fpr_intersectional))
