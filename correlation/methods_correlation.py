# -*- coding: utf-8 -*-
# Copyright (c) 2019-2021 Jessica López Espejel, Gaël de Chalendar and Jorge García Flores
# LIPN/USPN-CEA/LIST

# This file is part of GeSERA

# GeSERA is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GeSERA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Unoporuno.  If not, see <http://www.gnu.org/licenses/>.


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