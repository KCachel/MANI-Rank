"""
Borda Algorithm for Rank Aggregation
"""

#License: GNU GENERAL PUBLIC LICENSE
# Authors:  <kcachel@wpi.edu>

import numpy as np
def borda(ranks):
    item_list = list(np.unique(ranks[0,:]))
    bordaDict = {key: 0 for key in item_list}
    num_rankings, num_items = ranks.shape
    points_per_pos_legend = list(range(num_items - 1, -1, -1))

    for ranking in range(0,num_rankings):
        for item_pos in range(0,num_items):
            item = ranks[ranking,item_pos]
            bordaDict[item] += points_per_pos_legend[item_pos]

    candidates = list(bordaDict.keys())
    borda_scores = list(bordaDict.values())
    zip_scores_items = zip(borda_scores, candidates)
    sorted_pairs = sorted(zip_scores_items, reverse=True)
    sorted_list2 = [element for _, element in sorted_pairs]
    return sorted_list2



base_ranks = np.array([[ 1, 2, 3, 4, 5, 6],
                        [1, 3, 2, 4, 5, 6],
                        [5, 6, 1, 2, 3, 4],
                        [6, 5, 1, 2, 3, 4],
                        [1, 5, 6, 2, 3, 4]])
print(borda(base_ranks))