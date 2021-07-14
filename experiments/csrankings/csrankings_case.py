import multi_fair as mf
import numpy as np
import pandas as pd

base_ranks = np.load('cs_baseranks.npy').astype(int)
group_info_file = 'cs_groups.csv'

outputfile = 'csrankings_resultsgreedy.csv'

group_info = np.genfromtxt(group_info_file, delimiter=',', dtype=int).T  # transpose to be of attributes x candidates


intersectional = mf.make_intersectional_attribute(group_info, True)
groups_key = np.row_stack((group_info, intersectional))

location = []
type = []
intersection = []
method_group = []
rank_type = []
ranks = list(map(str, range(2000, 2021, 1) ))

for r in range(0,len(ranks)):
    rank = base_ranks[r, :]

    fpr_location = mf.fpr(rank, np.row_stack((groups_key[0], groups_key[1])))
    location.append(mf.rank_parity_score(fpr_location))

    fpr_type = mf.fpr(rank, np.row_stack((groups_key[0], groups_key[2])))
    type.append(mf.rank_parity_score(fpr_type))

    fpr_inter = mf.fpr(rank, np.row_stack((groups_key[0], groups_key[3])))
    intersection.append(mf.rank_parity_score(fpr_inter))

    method_group.append("base_rank")
    rank_type.append(ranks[r])

# Aggregation
###############
# Kemeny
##############
method_group.append("Kemeny")
rank_type.append("kemeny")
prob_result = mf.aggregate_rankings(base_ranks)
kemeny_soln = mf.find_solution(prob_result, base_ranks.shape[1])


fpr_location_kem = mf.fpr(kemeny_soln, np.row_stack((groups_key[0], groups_key[1])))
location.append(mf.rank_parity_score(fpr_location_kem))
print("fpr_location_kem Kem", fpr_location_kem)

fpr_type_kem = mf.fpr(kemeny_soln, np.row_stack((groups_key[0], groups_key[2])))
type.append(mf.rank_parity_score(fpr_type_kem))
print("fpr_type_kem Kem", fpr_type_kem)

# intersectional
fpr_inter_kem = mf.fpr(kemeny_soln, np.row_stack((groups_key[0], groups_key[3])))
intersection.append(mf.rank_parity_score(fpr_inter_kem))
print("fpr_inter Kem", fpr_inter_kem)

###############
# MFRA-IP
##############
#
method_group.append("Multi-Fair")
rank_type.append("Multi-Fair")
thres_vals = [.05, .05, .05]
prob_result = mf.aggregate_rankings_fair_ilp(base_ranks, groups_key, thres_vals, False)
fair_soln = mf.find_solution(prob_result, base_ranks.shape[1])

fpr_location = mf.fpr(fair_soln, np.row_stack((groups_key[0], groups_key[1])))
location.append(mf.rank_parity_score(fpr_location))
print("fpr_location", fpr_location)

fpr_type = mf.fpr(fair_soln, np.row_stack((groups_key[0], groups_key[2])))
type.append(mf.rank_parity_score(fpr_type))
print("fpr_race", fpr_type)

# intersectional
fpr_inter = mf.fpr(fair_soln, np.row_stack((groups_key[0], groups_key[3])))
intersection.append(mf.rank_parity_score(fpr_inter))
print("fpr_inter", fpr_inter)

###############
# Post-Correct
##############

pthresh_vals = [.05, .05]
ithresh = .05

greedy_soln = mf.correct_parity(np.asarray(kemeny_soln), group_info, pthresh_vals, ithresh)
method_group.append("greedy_fair")
rank_type.append("greedy_fair")


fpr_location = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[1])))
location.append(mf.rank_parity_score(fpr_location))
print("fpr_location", fpr_location)

fpr_type = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[2])))
type.append(mf.rank_parity_score(fpr_type))
print("fpr_race", fpr_type)


# intersectional
fpr_inter = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[3])))
intersection.append(mf.rank_parity_score(fpr_inter))
print("fpr_inter", fpr_inter)



dict = {'location': location, 'type': type, 'irp': intersection, 'method_group': method_group,
        'rank_type': rank_type}

results = pd.DataFrame(dict)
print(results)
results.to_csv(outputfile, index=False)