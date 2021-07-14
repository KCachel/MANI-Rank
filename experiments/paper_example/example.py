import multi_fair as mf
import numpy as np
import pandas as pd

outputfile = 'result.csv'

ranks = np.array([[9,  2,  4, 10,  5, 12,  3, 11,  8,   1,  13,   6,   7],
                   [8,  4, 13, 10,  7, 11,  2, 12,  5,   3,   9,   1,   6],
                   [8,  6,  5, 10, 11, 12,  1,  9,  7,   4 , 13,   2 ,  3],
                   [8,  4, 10, 11,  5,  9,  2, 12, 13,   1,   7,   3,   6]])
ranks = ranks - 1

groups = np.array([[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
                   [0, 0, 1, 1, 2, 2, 0, 0, 1, 1, 2, 2, 0]])

items = np.arange(0, 13)
intersectional = mf.make_intersectional_attribute(groups, True)
groups_inter = np.row_stack((items, intersectional))
groups_all_key = np.row_stack((groups, intersectional))

method = []
fpr1 = []
fpr2 = []
fprinter = []
atr1 = []
atr2 = []
atrinter = []
cf = []
result = []

#Kemeny Agg
prob_result = mf.aggregate_rankings(ranks)
soln = mf.find_solution(prob_result, 13)
result.append(soln)
ksoln = soln
method.append("kemeny")
cfval = mf.cost_fairness(ranks, ksoln, soln)
cf.append(cfval)
fpr_at1 = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[1])))
fpr1.append(fpr_at1)
at1_par = mf.rank_parity_score(fpr_at1)
atr1.append(at1_par)
fpr_at2 = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[2])))
fpr2.append(fpr_at2)
at2_par = mf.rank_parity_score(fpr_at2)
atr2.append(at2_par)
fpr_atinter = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[3])))
fprinter.append(fpr_atinter)
atinter_par = mf.rank_parity_score(fpr_atinter)
atrinter.append(atinter_par)

#Fair Agg
#top-level
prob_result = mf.aggregate_rankings_fair_ilp(ranks, groups, [.1, .1], False)
soln = mf.find_solution(prob_result, 13)
result.append(soln)
method.append("top")
cfval = mf.cost_fairness(ranks, ksoln, soln)
cf.append(cfval)
fpr_at1 = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[1])))
fpr1.append(fpr_at1)
at1_par = mf.rank_parity_score(fpr_at1)
atr1.append(at1_par)
fpr_at2 = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[2])))
fpr2.append(fpr_at2)
at2_par = mf.rank_parity_score(fpr_at2)
atr2.append(at2_par)
fpr_atinter = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[3])))
fprinter.append(fpr_atinter)
atinter_par = mf.rank_parity_score(fpr_atinter)
atrinter.append(atinter_par)


#inter-level
prob_result = mf.aggregate_rankings_fair_ilp(ranks, groups_inter, [.1], False)
soln = mf.find_solution(prob_result, 13)
result.append(soln)
method.append("inter")
cfval = mf.cost_fairness(ranks, ksoln, soln)
cf.append(cfval)
fpr_at1 = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[1])))
fpr1.append(fpr_at1)
at1_par = mf.rank_parity_score(fpr_at1)
atr1.append(at1_par)
fpr_at2 = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[2])))
fpr2.append(fpr_at2)
at2_par = mf.rank_parity_score(fpr_at2)
atr2.append(at2_par)
fpr_atinter = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[3])))
fprinter.append(fpr_atinter)
atinter_par = mf.rank_parity_score(fpr_atinter)
atrinter.append(atinter_par)

#both
prob_result = mf.aggregate_rankings_fair_ilp(ranks, groups_all_key, [.1, .1, .1], False)
soln = mf.find_solution(prob_result, 13)
result.append(soln)
method.append("multi")
cfval = mf.cost_fairness(ranks, ksoln, soln)
cf.append(cfval)
fpr_at1 = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[1])))
fpr1.append(fpr_at1)
at1_par = mf.rank_parity_score(fpr_at1)
atr1.append(at1_par)
fpr_at2 = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[2])))
fpr2.append(fpr_at2)
at2_par = mf.rank_parity_score(fpr_at2)
atr2.append(at2_par)
fpr_atinter = mf.fpr(soln, np.row_stack((groups_all_key[0], groups_all_key[3])))
fprinter.append(fpr_atinter)
atinter_par = mf.rank_parity_score(fpr_atinter)
atrinter.append(atinter_par)

dict = {'cf': cf, 'fpr1': fpr1, 'atr1': atr1, 'fpr2': fpr2,
        'atr2': atr2, 'fprinter': fprinter, 'atrinter': atrinter, 'method': method, 'result': result}
results = pd.DataFrame(dict)
print(results)
results.to_csv(outputfile, index=False)