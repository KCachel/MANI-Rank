import numpy as np
from multi_fair.metrics import *
from multi_fair.utils import *


def determine_group_from_item(candidates, grp_mem):
    """Create dictionary with key = candidate id and value = group ids"""
    group_item_dict = {}
    for var in np.unique(candidates):
        idx = var
        group_item_dict[(var)] = int(grp_mem[np.where(candidates == var)])
    return group_item_dict

def list_of_attribute_dicts(group_info):
    """Create list of dictionaries with key = candidate id and value = group ids"""
    num_attributes = group_info.shape[0] - 1
    attr_list_ofdicts = []
    for atr in range(0,num_attributes):
        attr_list_ofdicts.append(determine_group_from_item(group_info[0], group_info[atr+1]))
    return attr_list_ofdicts

def get_max_min_par(ranking, attribute_legend, group_info):
    max_parity = []
    max_parity_group_id = []
    min_parity = []
    min_parity_group_id = []
    num_attributes = len(attribute_legend)
    atrribute_groupids_sortedby_parity = []
    for atr in range(0,num_attributes):
        fprs = fpr(ranking, np.row_stack((group_info[0], group_info[atr+1])))
        max_parity.append(np.max(fprs))
        max_parity_group_id.append(np.where(fprs == np.max(fprs))[0][0]) #get group id
        min_parity.append(np.min(fprs))
        min_parity_group_id.append(np.where(fprs == np.min(fprs))[0][0]) #get group id
        atrribute_groupids_sortedby_parity.append(np.argsort(np.asarray(fprs)))

    return max_parity, min_parity, max_parity_group_id, min_parity_group_id, atrribute_groupids_sortedby_parity


def find_candidate_lowest(ranking, groups, group_legend):
    """ranking: current ranking
        groups: group looking for
        group_legend: dictionary lookup for candidates group id"""
    reversed_ranking = ranking[::-1] #reverse ranking
    for item in reversed_ranking:
        if group_legend[item] == groups:
            return item

def find_bottom_candidate(ranking, indx_top, attribute, attribute_legend, min_parity_group_id):

    mini_ranking = ranking[indx_top+1:]
    top = ranking[indx_top]
    for i in range(len(mini_ranking)):
        bottom = mini_ranking[i]
        indx_bottom = np.argwhere(ranking == bottom)[0][0]
        if attribute_legend[attribute][bottom] == min_parity_group_id:
            return bottom, indx_top, top, indx_bottom

    #did not find a bottom candidate matching criteria below current top, so find new top
    new_top = find_candidate_lowest(ranking[:indx_top], attribute_legend[attribute][top], attribute_legend[attribute])
    index_newtop = np.argwhere(ranking == new_top)[0][0]
    return find_bottom_candidate(ranking, index_newtop, attribute, attribute_legend, min_parity_group_id)


def correct_parity(ranking, group_info, pthres, ithres):
    """   A function for correcting the parity of a ranking
                :param ranking: A numpy array of current ranking
                :param group_info: A numpy array of group_info[0] = candidate ids, and row vectors for each protected attribute's group labels
                :param pthres: A python list of protected attribute ARP thresholds
                :param ithres: An int of IRP threshold
                :return: A numpy array of the corrected ranking"""

    y = []
    intersectional = make_intersectional_attribute(group_info, True)
    group_info = np.row_stack((group_info, intersectional))
    attribute_legend = list_of_attribute_dicts(group_info)
    corrected = ranking.copy()
    num_attributes = group_info.shape[0] - 1
    max_parity, min_parity, max_parity_group_id, min_parity_group_id, atrribute_groupids_sortedby_parity = get_max_min_par(corrected, attribute_legend, group_info)
    print("max - min parity per attribute at start", np.asarray(max_parity) - np.asarray(min_parity))
    swap_num = 0
    highest_min_parity_item = np.inf

    while not np.all(np.asarray(max_parity[:-1]) - np.asarray(min_parity[:-1]) <= pthres) or not np.all(np.asarray(max_parity[-1]) - np.asarray(min_parity[-1]) <= ithres):

        #bail out if swaps is greater than num_items
        if swap_num > ((len(ranking)*(len(ranking)-1))/2):
            print("Try increasing the allowable difference in parity")
            break
        attribute_to_correct = np.argmax(np.asarray(max_parity) - np.asarray(min_parity))
        top = find_candidate_lowest(corrected, max_parity_group_id[attribute_to_correct], attribute_legend[attribute_to_correct])
        index_top = np.argwhere(corrected == top)[0][0]
        bottom, index_top, top, index_bottom = find_bottom_candidate(corrected, index_top, attribute_to_correct, attribute_legend, min_parity_group_id[attribute_to_correct])

        #swap
        corrected[index_top] = bottom
        corrected[index_bottom] = top
        swap_num += 1
        max_parity, min_parity, max_parity_group_id, min_parity_group_id, atrribute_groupids_sortedby_parity = get_max_min_par(corrected, attribute_legend, group_info)
        print("corrected ranking", list(corrected))
        print("max parity", max_parity, "group id ", max_parity_group_id)
        print("min parity", min_parity, "group id ", min_parity_group_id)
        print("attribute corrected: ", attribute_to_correct)
        print("max - min parity per attribute ", np.asarray(max_parity) - np.asarray(min_parity))


    return corrected

