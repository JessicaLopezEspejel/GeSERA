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

import time
import threading
from utils import get_content
from utils import write_details
from utils import write_score
import numpy as np


def display_menu(refine_query, cut_off_point, sera, sera_type, poolq, sqr, pool, searcher, parser_query,
                 dic_automatic_summaries, num_files, name_f_scores, name_details, write_chunk, t0):
    num_file = 0
    sum_sera = 0
    sum_dis_sera = 0
    dic_score = dict()
    lst_details = []
    lst_average = []
    for path_candidate, lst_manual_summaries in dic_automatic_summaries.items():  # Candidate summary

        print('{}'.format(path_candidate))
        num_file += 1
        try:
            cntnt_cand = get_content(path_candidate, pool)[0]
        except Exception as error:
            cntnt_cand = " "

        nom_file = path_candidate.split('/')[-1]
        cad_scores = ''

        if nom_file in dic_score:
            continue

        if 'raw' in refine_query:  # Text without stop words and without numeric values
            dic_cand = poolq.apply_async(sqr.raw_text,
                                         args=(parser_query, searcher, path_candidate, cntnt_cand, cut_off_point))
        if 'np' in refine_query:   # Noun Phrases
            dic_cand = poolq.apply_async(sqr.noun_phrases,
                                         args=(parser_query, searcher, path_candidate, cntnt_cand, cut_off_point))
        if 'kw' in refine_query:  # Keywords
            dic_cand = poolq.apply_async(sqr.keywords,
                                         args=(parser_query, searcher, path_candidate, cntnt_cand, cut_off_point))
        if 'wikisera' in refine_query:  # Noun phrases, verb, adjective
            dic_cand = poolq.apply_async(sqr.noun_verb_adjective,
                                         args=(parser_query, searcher, path_candidate, cntnt_cand, cut_off_point))
        dic_candidate = dic_cand.get()

        lst_details.append(dic_candidate)

        for path_reference in lst_manual_summaries:  # Reference summaries

            avg_dis_sera, avg_sera = 0, 0
            try:
                cntnt_ref = get_content(path_reference, pool)[0]
            except Exception as error:
                cntnt_ref = " "

            # Type of text
            if 'raw' in refine_query:  # Text without stop words and without numeric values
                dic_ref = poolq.apply_async(sqr.raw_text,
                                            args=(parser_query, searcher, path_reference, cntnt_ref, cut_off_point))
            if 'np' in refine_query:  # Noun Phrases
                dic_ref = poolq.apply_async(sqr.noun_phrases,
                                            args=(parser_query, searcher, path_reference, cntnt_ref, cut_off_point))
            if 'kw' in refine_query:  # Keywords
                dic_ref = poolq.apply_async(sqr.keywords,
                                            args=(parser_query, searcher, path_reference, cntnt_ref, cut_off_point))
            if 'wikisera' in refine_query:  # noun phrases, verb, adjetive
                dic_ref = poolq.apply_async(sqr.noun_verb_adjective,
                                            args=(parser_query, searcher, path_reference, cntnt_ref, cut_off_point))
            dic_reference = dic_ref.get()

            lst_details.append(dic_reference)

            # Type of SERA
            if 'sera' in sera_type:
                file_num, score_sera = sera.sera_int(dic_reference, dic_candidate, cut_off_point)
                sum_sera += score_sera
                avg_sera = sum_sera / num_file
                cad_scores += str(score_sera) + ' '

            if 'dis' in sera_type:
                file_num, score_dis_sera = sera.dis_sera(dic_reference, dic_candidate)
                sum_dis_sera += score_dis_sera
                avg_dis_sera = sum_dis_sera / num_file
                cad_scores += str(score_dis_sera) + ' '

        avg_scores = np.average(list(map(float, cad_scores.split())))
        lst_average.append(avg_scores)
        dic_score[nom_file] = cad_scores + '{:.2f}'.format(avg_scores) #  str(round(avg_scores, 3))

        if num_file % write_chunk == 0 or num_file == num_files:
            t1 = time.time()
            print("  {}/{}. elapsed time : {}s".format(num_file, num_files, round(t1 - t0, 3)))
            writer_score = threading.Thread(target=write_score, args=(name_f_scores, dic_score))
            writer_score.start()
            writer_details = threading.Thread(target=write_details, args=(name_details, lst_details))
            writer_details.start()

    final_score = np.average(lst_average).tolist()
    print("\nFINAL SCORE: " + sera_type + '-' + refine_query + '-' + str(cut_off_point) + ': ' + '{:.2f}'.format(final_score) + '\n')