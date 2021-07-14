"""Script for Exam Case study
"""

#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>
import multi_fair as mf
import numpy as np
import pandas as pd

ranks_file = 'exam_base_rankings.csv'
group_info_file = 'exam_group_key.csv'


outputfile = 'exam_resultsgreedy.csv'


base_ranks = np.genfromtxt(ranks_file, delimiter=',', dtype=int).T #transpose to be of ranks x candidates

group_info = np.genfromtxt(group_info_file, delimiter=',', dtype=int).T #transpose to be of groups x candidates
intersectional = mf.make_intersectional_attribute(group_info, True)
groups_key = np.row_stack((group_info, intersectional))



gender = []
race = []
lunch = []
intersection = []
method_group = []
rank_type = []
ranks = ['math', 'reading', 'writing']

for r in range(len(ranks)):
    rank = base_ranks[r,:]

    fpr_gender = mf.fpr(rank, np.row_stack((groups_key[0], groups_key[1])))
    gender.append(mf.rank_parity_score(fpr_gender))

    fpr_race = mf.fpr(rank, np.row_stack((groups_key[0], groups_key[2])))
    race.append(mf.rank_parity_score(fpr_race))

    fpr_lunch = mf.fpr(rank, np.row_stack((groups_key[0], groups_key[3])))
    lunch.append(mf.rank_parity_score(fpr_lunch))

    fpr_inter = mf.fpr(rank, np.row_stack((groups_key[0], groups_key[4])))
    intersection.append(mf.rank_parity_score(fpr_inter))

    method_group.append("base_rank")
    rank_type.append(ranks[r])





#Aggregation
###############
# Kemeny
##############
# method_group.append("Kemeny")
# rank_type.append("kemeny")
# prob_result = mf.aggregate_rankings(base_ranks)
# kemeny_soln = mf.find_solution(prob_result, base_ranks.shape[1])
# print("kemeny_soln",kemeny_soln)
# fpr_gender_kem = mf.fpr(kemeny_soln, np.row_stack((groups_key[0], groups_key[1])))
# gender.append(mf.rank_parity_score(fpr_gender_kem))
# print("fpr_gender Kem", fpr_gender_kem)
#
#
# fpr_race_kem = mf.fpr(kemeny_soln, np.row_stack((groups_key[0], groups_key[2])))
# race.append(mf.rank_parity_score(fpr_race_kem))
# print("fpr_race Kem", fpr_race_kem)
#
# fpr_lunch_kem = mf.fpr(kemeny_soln, np.row_stack((groups_key[0], groups_key[3])))
# lunch.append(mf.rank_parity_score(fpr_lunch_kem))
# print("fpr_lunch Kem", fpr_lunch_kem)
#
# # intersectional
# fpr_inter_kem = mf.fpr(kemeny_soln, np.row_stack((groups_key[0], groups_key[4])))
# intersection.append(mf.rank_parity_score(fpr_inter_kem))
# print("fpr_inter Kem", fpr_inter_kem)

kemeny_soln = [48, 150, 46, 91, 83, 96, 39, 21, 60, 10, 194, 3, 32, 89, 140, 147, 40, 110, 25, 113, 16, 28, 145, 93, 174, 116, 80, 102, 157, 192, 179, 95, 175, 183, 56, 66, 112, 54, 59, 67, 33, 120, 70, 98, 129, 107, 172, 109, 31, 69, 86, 139, 144, 197, 79, 178, 163, 166, 148, 81, 184, 126, 173, 57, 58, 169, 111, 15, 121, 154, 168, 143, 176, 43, 90, 118, 119, 122, 6, 1, 30, 141, 186, 5, 49, 14, 100, 35, 50, 34, 18, 193, 156, 191, 124, 74, 131, 195, 45, 88, 159, 132, 76, 85, 13, 94, 142, 125, 136, 138, 167, 130, 181, 52, 87, 19, 72, 128, 17, 24, 114, 164, 75, 190, 9, 36, 42, 117, 4, 65, 0, 115, 177, 99, 135, 62, 123, 162, 160, 64, 82, 11, 77, 47, 8, 71, 146, 149, 158, 63, 134, 161, 105, 108, 182, 55, 196, 7, 188, 2, 92, 189, 84, 26, 127, 165, 51, 199, 23, 29, 37, 68, 133, 198, 104, 12, 38, 41, 44, 97, 137, 153, 103, 73, 61, 155, 170, 22, 78, 152, 101, 185, 180, 20, 187, 106, 27, 53, 151, 171]
#
# ###############
# # Multi_Fair constraints (intersectional + protected attribute level)
# ##############
#
# method_group.append("Multi-Fair")
# rank_type.append("Multi-Fair")
# thres_vals = [.05, .05, .05, .05]
# prob_result = mf.aggregate_rankings_fair_ilp(base_ranks, groups_key, thres_vals, False)
# fair_soln = mf.find_solution(prob_result, base_ranks.shape[1])
#
#
# fpr_gender = mf.fpr(fair_soln, np.row_stack((groups_key[0], groups_key[1])))
# gender.append(mf.rank_parity_score(fpr_gender))
# print("fpr_gender", fpr_gender)
#
#
# fpr_race = mf.fpr(fair_soln, np.row_stack((groups_key[0], groups_key[2])))
# race.append(mf.rank_parity_score(fpr_race))
# print("fpr_race", fpr_race)
#
# fpr_lunch = mf.fpr(fair_soln, np.row_stack((groups_key[0], groups_key[3])))
# lunch.append(mf.rank_parity_score(fpr_lunch))
# print("fpr_lunch", fpr_lunch)
#
# # intersectional
# fpr_inter = mf.fpr(fair_soln, np.row_stack((groups_key[0], groups_key[4])))
# intersection.append(mf.rank_parity_score(fpr_inter))
# print("fpr_inter", fpr_inter)

###############
# Multi_Fair constraints (greedy)
##############

pthresh_vals = [.05, .05, .05]
ithresh = .05
greedy_soln = mf.correct_parity(np.asarray(kemeny_soln), group_info, pthresh_vals, ithresh)
method_group.append("greedy_fair")
rank_type.append("greedy_fair")

print("greedy fair ","done")

fpr_gender = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[1])))
gender.append(mf.rank_parity_score(fpr_gender))
print("fpr_gender", fpr_gender)


fpr_race = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[2])))
race.append(mf.rank_parity_score(fpr_race))
print("fpr_race", fpr_race)

fpr_lunch = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[3])))
lunch.append(mf.rank_parity_score(fpr_lunch))
print("fpr_lunch", fpr_lunch)

# intersectional parity
fpr_inter = mf.fpr(greedy_soln, np.row_stack((groups_key[0], groups_key[4])))
intersection.append(mf.rank_parity_score(fpr_inter))

dict = {'gender': gender, 'race': race, 'lunch': lunch, 'irp': intersection, 'method_group': method_group, 'rank_type': rank_type}



results = pd.DataFrame(dict)
print(results)
results.to_csv(outputfile,index=False)