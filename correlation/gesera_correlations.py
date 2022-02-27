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


import argparse
import os
from methods_correlation import spearman_correlation
from methods_correlation import pearson_correlation
from methods_correlation import kendall_correlation
from utils import *


def main():
    path_correlation = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument('-sera_file', type=str, default=path_correlation +'/data_example/ordered_score_wiki_0-4840.txt')
    parser.add_argument('-file_scores', type=str, default=path_correlation + '/data_example/SCORES_TAC2009.txt')

    opt = parser.parse_args()

    print(opt.sera_file)
    print(opt.file_scores)

    # ----------------------------- PYRAMID -----------------------------s
    lst_pyr_4m, lst_pyr_3m = read_pyramid(opt.file_scores)
    labels_pyramid = ["4m", "3m"]
    lst_pyramid = [lst_pyr_4m, lst_pyr_3m]


    # ------------------------------ ROUGE ------------------------------
    lst_rouge1_R, lst_rouge1_P, lst_rouge1_F = read_ROUGE_1(opt.file_scores)
    lst_rouge2_R, lst_rouge2_P, lst_rouge2_F = read_ROUGE_2(opt.file_scores)
    lst_rouge3_R, lst_rouge3_P, lst_rouge3_F = read_ROUGE_3(opt.file_scores)
    lst_rouge4_R, lst_rouge4_P, lst_rouge4_F = read_ROUGE_4(opt.file_scores)
    lst_rougeL_R, lst_rougeL_P, lst_rougeL_F = read_ROUGE_L(opt.file_scores)
    lst_rougeW_R, lst_rougeW_P, lst_rougeW_F = read_ROUGE_W(opt.file_scores)
    lst_rougeSU4_R, lst_rougeSU4_P, lst_rougeSU4_F = read_ROUGE_SU4(opt.file_scores)

    labels_rouge = ["R1", "R2", "R3", "RL", "RW", "RSU4"]
    lst_rouge_F = [lst_rouge1_F, lst_rouge2_F, lst_rouge3_F, lst_rougeL_F, lst_rougeW_F, lst_rougeSU4_F]
    lst_rouge_P = [lst_rouge1_P, lst_rouge2_P, lst_rouge3_P, lst_rougeL_P, lst_rougeW_P, lst_rougeSU4_P]
    lst_rouge_R = [lst_rouge1_R, lst_rouge2_R, lst_rouge3_R, lst_rougeL_R, lst_rougeW_R, lst_rougeSU4_R]

    # ------------------------------ SERA ------------------------------

    lst_M1_M2_M3_M4 = SERA_M1_M2_M3_M4(opt.sera_file)
    labels_SERA = ['M1_M2_M3_M4']
    lst_SERA = [lst_M1_M2_M3_M4]

    for pyramid, label_pyramid in zip(lst_pyramid, labels_pyramid):

        for sera_value, label_SERA in zip(lst_SERA, labels_SERA):
            corr_pearson, _ = pearson_correlation(pyramid, sera_value)
            corr_spearman, _ = spearman_correlation(pyramid, sera_value)
            corr_kendall, _ = kendall_correlation(pyramid, sera_value)
            print('{0} {1} Pearson: {2:.3f} Spearman: {3:.3f} Kendall: {4:.3f}'.format(label_pyramid, label_SERA,
                                                                    corr_pearson, corr_spearman, corr_kendall))

        # for rouge_F, rouge_P, rouge_R, label_rouge in zip(lst_rouge_F, lst_rouge_P, lst_rouge_R, labels_rouge):
        #     corr_pearson_F, _ = pearson_correlation(pyramid, rouge_F)
        #     corr_pearson_P, _ = pearson_correlation(pyramid, rouge_P)
        #     corr_pearson_R, _ = pearson_correlation(pyramid, rouge_R)
        #     print('{0} {1} Pearson F: {2:.3f} Pearson P: {3:.3f} Pearson R: {4:.3f}'.format(label_pyramid, label_rouge,
        #                                                                                     corr_pearson_F,
        #                                                                                     corr_pearson_P,
        #                                                                                     corr_pearson_R))
        #
        #     corr_spearman_F, _ = spearman_correlation(pyramid, rouge_F)
        #     corr_spearman_P, _ = spearman_correlation(pyramid, rouge_P)
        #     corr_spearman_R, _ = spearman_correlation(pyramid, rouge_R)
        #     print(
        #         '{0} {1} Spearman F: {2:.3f} Spearman P: {3:.3f} Spearman R: {4:.3f}'.format(label_pyramid, label_rouge,
        #                                                                                      corr_spearman_F,
        #                                                                                      corr_spearman_P,
        #                                                                                      corr_spearman_R))  #
        #
        #     corr_kendall_F, _ = kendall_correlation(pyramid, rouge_F)
        #     corr_kendall_P, _ = kendall_correlation(pyramid, rouge_P)
        #     corr_kendall_R, _ = kendall_correlation(pyramid, rouge_R)
        #     print('{0} {1} Kendall F: {2:.3f} Kendall P: {3:.3f} Kendall R: {4:.3f}'.format(label_pyramid, label_rouge,
        #                                                                                     corr_kendall_F,
        #                                                                                     corr_kendall_P,
        #                                                                                     corr_kendall_R))


if __name__ == '__main__':
    main()