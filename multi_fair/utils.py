"""
Helper functions
"""
#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>


import numpy as np
from itertools import combinations
from collections import Counter
from more_itertools import unique_everseen

def all_pair_precedence_weight(ranks):
    """construct precedence matrix"""
    n_voters, n_candidates = ranks.shape
    edge_weights = np.zeros((n_candidates, n_candidates))

    pwin_cand = np.unique(ranks[0]).tolist()
    plose_cand = np.unique(ranks[0]).tolist()
    combos = [(i, j) for i in pwin_cand for j in plose_cand]
    #for i, j in combinations(range(n_candidates), 2):
    for combo in combos:
        i = combo[0]
        j = combo[1]
        h_ij = 0 #prefer i to j
        h_ji = 0 #prefer j to i
        for r in range(n_voters):
            if list(ranks[r]).index(i) > list(ranks[r]).index(j):
                h_ij += 1*(r+1)
            else:
                h_ji += 1*(r+1)

        edge_weights[i, j] = h_ij
        edge_weights[j, i] = h_ji
        np.fill_diagonal(edge_weights, 0)
    return edge_weights  # index [i,j] shows how many prefer j over i

def all_pair_precedence(ranks):
    """construct precedence matrix"""
    n_voters, n_candidates = ranks.shape
    edge_weights = np.zeros((n_candidates, n_candidates))

    pwin_cand = np.unique(ranks[0]).tolist()
    plose_cand = np.unique(ranks[0]).tolist()
    combos = [(i, j) for i in pwin_cand for j in plose_cand]
    #for i, j in combinations(range(n_candidates), 2):
    for combo in combos:
        i = combo[0]
        j = combo[1]
        h_ij = 0 #prefer i to j
        h_ji = 0 #prefer j to i
        for r in range(n_voters):
            #if list(ranks[r]).index(i) > list(ranks[r]).index(j):
            if np.argwhere(ranks[r] == i)[0][0] > np.argwhere(ranks[r] == j)[0][0]:
                h_ij += 1
            else:
                h_ji += 1

        edge_weights[i, j] = h_ij
        edge_weights[j, i] = h_ji
        np.fill_diagonal(edge_weights, 0)
    return edge_weights  # index [i,j] shows how many prefer j over i

def all_pair_precedence_fair(ranks):
    """construct precedence matrix"""
    n_voters, n_candidates = ranks.shape
    edge_weights = cp.zeros((n_candidates, n_candidates))

    pwin_cand = cp.unique(ranks[0]).tolist()
    plose_cand = cp.unique(ranks[0]).tolist()
    combos = [(i, j) for i in pwin_cand for j in plose_cand]
    #for i, j in combinations(range(n_candidates), 2):
    for combo in combos:
        i = combo[0]
        j = combo[1]
        h_ij = 0 #prefer i to j
        h_ji = 0 #prefer j to i
        for r in range(n_voters):
            #if list(ranks[r]).index(i) > list(ranks[r]).index(j):
            if cp.argwhere(ranks[r] == i)[0][0] > cp.argwhere(ranks[r] == j)[0][0]:
                h_ij += 1
            else:
                h_ji += 1

        edge_weights[i, j] = h_ij
        edge_weights[j, i] = h_ji
        cp.fill_diagonal(edge_weights, 0)
    return edge_weights  # index [i,j] shows how many prefer j over i

def find_solution(prob, num_candidates):
    """   Compute solution (list of candidates from PuLP binary variables.
                :param prob: A PuLP problem variable
                :param num_candidates: int number of candidates in problem.
                :return solution: python list ranking over candidates"""

    #collect variables that are true
    true_vars = [v.name for v in prob.variables() if v.varValue == 1 and v.name != 'Y']
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

    return np.asarray(solution)


def ranking_with_group_labels(ranking, candidates, group_labels):
    ranking_group_labels = []
    for cand in range(0,len(ranking)):
        ranking_group_labels.append(group_labels[np.where(candidates == ranking[cand])[0][0]])
    return ranking_group_labels


def kendalltau_dist(rank_a, rank_b):
    tau = 0
    n_candidates = len(rank_a)
    for i, j in combinations(range(n_candidates), 2):
        tau += (np.sign(rank_a[i] - rank_a[j]) ==
                -np.sign(rank_b[i] - rank_b[j]))
    return tau

def make_intersectional_attribute(groups, printgrps):
    """groups = attributes X candidates numpy, first row - items, then each subsequent is an attribute

    """
    groups = groups[1:,]
    combos = np.unique(groups, axis = 1)
    num_candidates = groups.shape[1]
    num_intersectional_groups = combos.shape[1]
    if printgrps:
        for i in range(0,num_intersectional_groups):
            print("intersectional group ", i, " represents ", list(combos[:,i]))
    intersectional = [np.where((combos.T == list(groups[:,i])).all(axis=1))[0][0]    for i in range(0,num_candidates)]
    return np.asarray(intersectional)

def determine_group_identity(candidates, grp_mem):
    """Create dictionary with key = group id and value = candidate ids"""
    group_id_dict = {}
    for var in np.unique(grp_mem):
        idx = np.where(grp_mem == var)
        group_id_dict[(var)] = [str(item) for item in candidates[idx].tolist()]  # make it a list of str
    return group_id_dict

def candidates_by_group(candidates, grp_mem):
    """Create dictionary with key = group id and value = candidate ids
    ints instead of strings"""
    group_id_dict = {}
    for var in np.unique(grp_mem):
        idx = np.where(grp_mem == var)
        group_id_dict[(var)] = [item for item in candidates[idx].tolist()]  # make it a list of int
    return group_id_dict


def pair_count_at_position_array(num_candidates):
    return list(np.arange(num_candidates - 1, -1, -1))

def pair_count(num_candidates):
    return (num_candidates*(num_candidates - 1))/2

def count_pairwise_disagreements(base_rankings, ranking):
    disagree_count = 0
    precedence_mat = all_pair_precedence(base_rankings)
    positions = len(ranking)
    for pos in range(positions):
        top_candidate = ranking[pos]
        bottom_candidates = ranking[pos+1: positions]
        for x in bottom_candidates:
            disagree_count += precedence_mat[top_candidate,x]
    return disagree_count

def kendall_tau_distance(order_a, order_b):
    pairs = combinations(range(1, len(order_a)+1), 2)
    distance = 0
    for x, y in pairs:
        a = order_a.index(x) - order_a.index(y)
        b = order_b.index(x) - order_b.index(y)
        if a * b < 0:
            distance += 1
    return distance

def avg_kt_distance(base_rankings, ranking):
    #base_rankings, ranking are np arrays
    num_rankings, num_items = base_rankings.shape
    ranking_list = list(ranking)
    kt_s = np.zeros(num_rankings)
    for ranking_i in range(0,num_rankings):
        base_rank = list(base_rankings[ranking_i,:])
        kt_s[ranking_i] = kendall_tau_distance(base_rank, ranking_list)

    avg_kt = np.mean(kt_s)
    return avg_kt