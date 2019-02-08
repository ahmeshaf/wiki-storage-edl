"""
This files will hold the static functions to generate the common link relevancy features
"""

from math import log


NGD_DEFAULT = 5.0
PMI_DEFAULT = -1.0
W_SIZE = 5753718
def ngd(l1, l2, W=W_SIZE):
    '''
    Normalized google distance
    :param l1: set/list of links L1
    :param l2: set/list of links L2
    :param W: total links in our training set or Wikipedia size (constant)
    :return:
    '''
    l1_set = set(l1)
    l2_set = set(l2)
    len_l1 = len(l1_set)
    len_l2 = len(l2_set)
    len_l1_in_l2 = len(l1_set.intersection(l2_set))
    if len_l1 == 0 or len_l2 == 0 or len_l1_in_l2 == 0:
        return NGD_DEFAULT
    else:
        return (log(max(len_l1, len_l2)) - log(len(l1_set.intersection(l2_set))))/(log(W) - log(min(len_l1, len_l2)))

def npmi(l1, l2, W=5753718):
    '''
    Pointwise mutual information
    :param l1: set/list of links L1
    :param l2: set/list of links L2
    :param W: total links in our training set or Wikipedia size (constant)
    :return: 1 if highly corelated, 0 if random, -1 if not correlated at all
    '''
    l1_set = set(l1)
    l2_set = set(l2)
    len_l1 = len(l1_set)
    len_l2 = len(l2_set)
    p1 = len_l1/W
    p2 = len_l2/W
    p1p2 = len(l1_set.intersection(l2_set))/W
    if p1 == 0 or p2 == 0 or p1p2 == 0.:
        return PMI_DEFAULT
    else:
        return log(p1 * p2)/log(p1p2) - 1

def tss(l1, l2, W=5753718, alpha=0.25):
    '''
    Twitter semantic similarity
    :param l1: links
    :param l2: links
    :param alpha: scaling constant (default = 0.25)
    :return: value
    '''
    l1_set = set(l1)
    l2_set = set(l2)
    len_l1 = len(l1_set)
    len_l2 = len(l2_set)
    if len_l1 == 0 or len_l2 == 0:
        return 0
    return (len(l1_set.intersection(l2_set))/max(len_l1, len_l2))**alpha


def js(l1, l2, W=5753718):
    '''
    Good 'ol Jaccard Similarity: (A cup B)/(A U B)
    :param l1: set/list of links L1
    :param l2: set/list of links L2
    :return:
    '''
    l1_set = set(l1)
    l2_set = set(l2)
    len_l1_or_l2 = len(l1_set.union(l2_set))
    len_l1_and_l2 = len(l1_set.intersection(l2_set))
    if len_l1_and_l2 == 0 or len_l1_or_l2 == 0:
        return 0.
    else:
        return len_l1_and_l2/len_l1_or_l2
