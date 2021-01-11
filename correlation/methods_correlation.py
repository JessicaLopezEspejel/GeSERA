#!/usr/bin/env python3

import numpy as np
from scipy.stats import spearmanr
from scipy.stats import kendalltau
from scipy.stats import pearsonr


def spearman_correlation(x, y):
    """ Return:
    - correlation: if there are two arrays(x,y) we will get a spearman correlation.
    If we have more than two arrays, we wil get a matrix.
    - pval: if is none, the hypothesis of two sets are uncorrelated.
    """
    correlation, pval = spearmanr(x, y)
    return correlation, pval


def pearson_correlation(x, y):
    """ It results are between [-1, 1] - 0 means no correlation.
    Positive correlations imply that as x increases, so does y.
    Negative correlations imply that as x increases, y decreases.
    """
    x = np.array(x).astype(np.float)
    y = np.array(y).astype(np.float)
    corr, p_value = pearsonr(x, y)
    return corr, p_value


def kendall_correlation(x, y):
    tau, p_value = kendalltau(x, y)
    return tau, p_value