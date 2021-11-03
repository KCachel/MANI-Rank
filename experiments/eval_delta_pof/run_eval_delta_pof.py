"""
Script for evaluating methods on Mallows datasets
"""


#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>
# Authors: Kathleen Cachel <kcachel@wpi.edu>
import sys

# append the path of the parent directory
sys.path.append("..")
import multi_fair as mf
import numpy as np
import pandas as pd
import sys
import time

def run_evaluation_of_delta(mallows_dataset):
    #mallows_dataset: medf, lowf, highf
    if mallows_dataset == "lowf":
        data_filenames = [r"\lowf\Rtheta_2.csv",
                          r"\lowf\Rtheta_4.csv",
                          r"\lowf\Rtheta_6.csv",
                          r"C\lowf\Rtheta_8.csv",]
        levels = ['lowf', 'lowf', 'lowf', 'lowf']
        thetas = [.2, .4, .6, .8]

        outputfile = r"Malowsresults_delta_pof_lowf.csv"
    if mallows_dataset == "medf":
        data_filenames = [r"\medf\Rtheta_2.csv",
                          r"\medf\Rtheta_4.csv",
                          r"\medf\Rtheta_6.csv",
                          r"\medf\Rtheta_8.csv"]
        levels = ['medf', 'medf', 'medf', 'medf']
        thetas = [.2, .4, .6, .8]
        outputfile = r"Malowsresults_delta_pof_medf.csv"
    if mallows_dataset == "highf":
        data_filenames = [r"C\highf\Rtheta_2.csv",
                          r"\highf\Rtheta_4.csv",
                          r"\highf\Rtheta_6.csv",
                          r"\highf\Rtheta_8.csv"]
        levels = ['highf', 'highf', 'highf', 'highf']
        thetas = [.2, .4, .6, .8]
        outputfile = r"Malowsresults_delta_pof_highf.csv"

    pthres_ = [.1, .1]
    ithres_ = .1
    thresh_fairilp_ = [.1, .1, .1]
    #group information
    NUM_GROUPS = 15
    GRP_SZ = 6
    atr1 = np.hstack((np.zeros(30, dtype=int), np.ones(30, dtype=int), np.ones(30, dtype=int) * 2))
    atr2 = np.tile((0, 1, 2, 3, 4), 18)
    groups = np.row_stack((atr1, atr2))
    items = np.arange(0, GRP_SZ * NUM_GROUPS)
    group_info = np.row_stack((items, groups))
    intersectional = mf.make_intersectional_attribute(group_info, True)
    groups_inter = np.row_stack((items, intersectional))
    groups_info_with_inter = np.row_stack((group_info, intersectional))

    method = []
    theta_value = []
    level = []
    fpr_gender = []
    fpr_race = []
    arp_gender = []
    arp_race = []
    fpr_inter = []
    IRP = []
    delta = []
    pd_loss = []
    POF_pd = []

    #####################
    # METHODS
    #####################
    for i in range(len(thetas)):
        base_ranks = np.genfromtxt(data_filenames[i], delimiter=',', dtype=int)
        for t in range(0,5):
            thresh_fairilp = list(np.asarray(thresh_fairilp_) * (t + 1))
            pthres = list(np.asarray(pthres_) * (t + 1))
            ithres = ithres_ * (t + 1)



            # KEMENY
            start_time = time.time()
            prob_result = mf.aggregate_rankings(base_ranks)
            kemeny_soln = mf.find_solution(prob_result, GRP_SZ * NUM_GROUPS)
            end_time = time.time()
            total_time = end_time - start_time
            print("kemeny", kemeny_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(kemeny_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(kemeny_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(kemeny_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Kemeny")
            theta_value.append(thetas[i])
            level.append(levels[i])
            fpr_gender.append(fpr_a1)
            fpr_race.append(fpr_a2)
            arp_gender.append(ARP_a1)
            arp_race.append(ARP_a2)
            fpr_inter.append(FPR_inter)
            IRP.append(irp_val)
            delta.append(ithres)
            pd_loss.append(mf.pd_loss(base_ranks, kemeny_soln))
            POF_pd.append(mf.POF_pd(base_ranks, kemeny_soln, kemeny_soln))



            #FAIR FOOTRULE
            start_time = time.time()
            fair_soln = mf.aggregate_footrule(base_ranks, groups_info_with_inter, pthres, ithres)

            end_time = time.time()
            total_time = end_time - start_time
            print("fair footrule", fair_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Fair_Footrule")
            theta_value.append(thetas[i])
            level.append(levels[i])
            fpr_gender.append(fpr_a1)
            fpr_race.append(fpr_a2)
            arp_gender.append(ARP_a1)
            arp_race.append(ARP_a2)
            fpr_inter.append(FPR_inter)
            IRP.append(irp_val)
            delta.append(ithres)
            pd_loss.append(mf.pd_loss(base_ranks, fair_soln))
            POF_pd.append(mf.POF_pd(base_ranks, kemeny_soln, fair_soln))

            # FAIR ILP
            start_time = time.time()
            prob_result = mf.aggregate_rankings_fair_ilp(base_ranks, group_info, thresh_fairilp, True)
            fair_soln = mf.find_solution(prob_result, GRP_SZ * NUM_GROUPS)
            end_time = time.time()
            total_time = end_time - start_time
            print("fair ilp", fair_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Fair_Kemeny")
            theta_value.append(thetas[i])
            level.append(levels[i])
            fpr_gender.append(fpr_a1)
            fpr_race.append(fpr_a2)
            arp_gender.append(ARP_a1)
            arp_race.append(ARP_a2)
            fpr_inter.append(FPR_inter)
            IRP.append(irp_val)
            delta.append(ithres)
            pd_loss.append(mf.pd_loss(base_ranks, fair_soln))
            POF_pd.append(mf.POF_pd(base_ranks, kemeny_soln, fair_soln))



            # FAIR SCHULZE
            start_time = time.time()
            fair_soln = mf.fair_schulze(base_ranks, groups_info_with_inter, pthres, ithres)
            end_time = time.time()
            total_time = end_time - start_time
            print("schulze", fair_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Fair_Schulze")
            theta_value.append(thetas[i])
            level.append(levels[i])
            fpr_gender.append(fpr_a1)
            fpr_race.append(fpr_a2)
            arp_gender.append(ARP_a1)
            arp_race.append(ARP_a2)
            fpr_inter.append(FPR_inter)
            IRP.append(irp_val)
            delta.append(ithres)
            pd_loss.append(mf.pd_loss(base_ranks, fair_soln))
            POF_pd.append(mf.POF_pd(base_ranks, kemeny_soln, fair_soln))

            # FAIR BORDA
            start_time = time.time()
            fair_soln = mf.fair_borda(base_ranks, groups_info_with_inter, pthres, ithres)
            end_time = time.time()
            total_time = end_time - start_time
            print("borda", fair_soln)


            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Fair_Borda")
            theta_value.append(thetas[i])
            level.append(levels[i])
            fpr_gender.append(fpr_a1)
            fpr_race.append(fpr_a2)
            arp_gender.append(ARP_a1)
            arp_race.append(ARP_a2)
            fpr_inter.append(FPR_inter)
            IRP.append(irp_val)
            delta.append(ithres)
            pd_loss.append(mf.pd_loss(base_ranks, fair_soln))
            POF_pd.append(mf.POF_pd(base_ranks, kemeny_soln, fair_soln))

            # FAIR COPELAND
            start_time = time.time()
            fair_soln = mf.fair_copeland(base_ranks, groups_info_with_inter, pthres, ithres)
            end_time = time.time()
            total_time = end_time - start_time
            print("COPELAND", fair_soln)

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Fair_Copeland")
            theta_value.append(thetas[i])
            level.append(levels[i])
            fpr_gender.append(fpr_a1)
            fpr_race.append(fpr_a2)
            arp_gender.append(ARP_a1)
            arp_race.append(ARP_a2)
            fpr_inter.append(FPR_inter)
            IRP.append(irp_val)
            delta.append(ithres)
            pd_loss.append(mf.pd_loss(base_ranks, fair_soln))
            POF_pd.append(mf.POF_pd(base_ranks, kemeny_soln, fair_soln))

            # CORRECT FAIREST PERM
            start_time = time.time()
            fair_soln = mf.correct_fairest_perm(base_ranks, groups_info_with_inter, pthres, ithres, True)
            end_time = time.time()
            total_time = end_time - start_time
            print("correct fairest perm",fair_soln )

            # attribute 1 parity
            fpr_a1 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[1])))
            ARP_a1 = mf.rank_parity_score(fpr_a1)

            # attribute 2 parity
            fpr_a2 = mf.fpr(fair_soln, np.row_stack((group_info[0], group_info[2])))
            ARP_a2 = mf.rank_parity_score(fpr_a2)

            # intersectional parity
            FPR_inter = mf.fpr(fair_soln, np.row_stack((groups_info_with_inter[0], groups_info_with_inter[3])))
            irp_val = mf.rank_parity_score(FPR_inter)
            method.append("Correct_Fairest_Perm")
            theta_value.append(thetas[i])
            level.append(levels[i])
            fpr_gender.append(fpr_a1)
            fpr_race.append(fpr_a2)
            arp_gender.append(ARP_a1)
            arp_race.append(ARP_a2)
            fpr_inter.append(FPR_inter)
            IRP.append(irp_val)
            delta.append(ithres)
            pd_loss.append(mf.pd_loss(base_ranks, fair_soln))
            POF_pd.append(mf.POF_pd(base_ranks, kemeny_soln, fair_soln))

            # dictionary of lists
            dict = {'method': method, 'theta_value': theta_value, 'level': level,
                    'fpr_gender': fpr_gender, 'fpr_race': fpr_race, 'arp_gender': arp_gender,
                    'arp_race': arp_race, 'fpr_inter': fpr_inter, 'IRP': IRP, 'delta': delta,
                    'pd_loss': pd_loss, 'POF_pd': POF_pd}


            results = pd.DataFrame(dict)
            print(results)
            results.to_csv(outputfile, index=False)
        # dictionary of lists

        dict = {'method': method, 'theta_value': theta_value, 'level': level,
                'fpr_gender': fpr_gender, 'fpr_race': fpr_race, 'arp_gender': arp_gender,
                'arp_race': arp_race, 'fpr_inter': fpr_inter, 'IRP': IRP,
                'delta': delta, 'pd_loss': pd_loss, 'POF_pd': POF_pd}

        results = pd.DataFrame(dict)
        print(results)
        results.to_csv(outputfile, index=False)

run_evaluation_of_delta("lowf")