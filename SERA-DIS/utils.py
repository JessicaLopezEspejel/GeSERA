# -*- coding: utf-8 -*-
## Copyright (c) 2019-2021 Jessica López Espejel, Gaël de Chalendar and Jorge García Flores
## LIPN/USPN-CEA/LIST

## This file is part of wikiSERA

##     wikiSERA is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.

##     wikiSERA is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with Unoporuno.  If not, see <http://www.gnu.org/licenses/>.
##

from __future__ import division
import numpy as np
from math import log, fabs
from collections import defaultdict


def read_file(file_name):
    dic_ref, dic_cand, dic_results = defaultdict(lambda: []), defaultdict(lambda: []), defaultdict(lambda: [])
    cont = 0
    with open(file_name, 'r') as file:
        for line in file:
            line = line.rstrip('\r\n').split('\t')
            if len(line) == 2:
                ID_file = line[0].split('.')
                name_file = ID_file[0] + '.' + ID_file[-1]
                lst_docs = line[-1][1:-1].replace(',', '').replace("'", '').split()

                if name_file.split('.')[-1].isdigit():  # and cont % 5 == 0:
                    name_cand = name_file
                    dic_cand[name_cand] = lst_docs
                    # print(name_cand, dic_cand[name_cand])
                if not name_file.split('.')[-1].isdigit():
                    dic_ref[name_file] = lst_docs
                    # print(name_file, dic_ref[name_file])

                if len(dic_ref.values()) == 1:
                    score = dis_sera(dic_cand, dic_ref)
                    score = '{:.3f}'.format(score)
                    dic_results[name_cand].append(score)
                    dic_ref = defaultdict(lambda: [])

            if len(line) == 1:
                dic_cand = defaultdict(lambda: [])
            cont += 1
    return dic_results


def dis_sera(dic_results_candidate, dic_results_reference):
    score = 0
    Dmax = 1 * (1 / log(2))
    div = 0

    for (ID_ref, lst_files_ref), (ID_cand, lst_files_cand) in zip(dic_results_reference.items(),
                                                                  dic_results_candidate.items()):
        D_max = 0
        for index_candidate, element_candidate in enumerate(lst_files_cand):
            for index_reference, element_reference in enumerate(lst_files_ref):
                if element_candidate == element_reference:
                    div += 1 / (log(fabs(index_candidate - index_reference) + 2))
            D_max += 1 / (log(2))
        try:
            score = div / D_max
        except Exception as error:
            score = 0.0
    return score


def write_file(path_save_file, dic_results):
    with open(path_save_file, 'w') as file:
        for key, value in dic_results.items():
            avg_scores = np.average(list(map(float, value))).tolist()
            file.write(key + '\t' + ' '.join(value) + ' ' + '{:.2f}'.format(avg_scores) + '\n')