#!/usr/bin/env python3
import sys
import numpy as np
from collections import defaultdict


def read_pyramid(file_scores):
    dic_pyr_4m,   dic_pyr_3m = defaultdict(lambda: []), defaultdict(lambda: [])
    with open(file_scores, 'r') as file:
        for line in file:
            line = line.split()
            docs = line[0].split('.')[1]
            dic_pyr_4m[docs].append(float(line[1]))
            dic_pyr_3m[docs].append(float(line[2]))
    lst_pyr_4m,   lst_pyr_3m = [], []
    for key, val in dic_pyr_4m.items():
        lst_pyr_4m.append(np.average(val, axis=0))
    for key, val in dic_pyr_3m.items():
        lst_pyr_3m.append(np.average(val, axis=0))
    return lst_pyr_4m, lst_pyr_3m


def read_ROUGE(file_scores, from_column):
    dic_rouge_R, dic_rouge_P, dic_rouge_F = defaultdict(lambda: []), defaultdict(lambda: []), defaultdict(lambda: [])
    with open(file_scores, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                line = line.split()
                docs = line[0].split('.')[1]
                dic_rouge_R[docs].append(float(line[from_column+0].split(':')[-1]))
                dic_rouge_P[docs].append(float(line[from_column+1].split(':')[-1]))
                dic_rouge_F[docs].append(float(line[from_column+2].split(':')[-1]))
    lst_rouge_R, lst_rouge_P, lst_rouge_F =  [], [], []
    for key, val in dic_rouge_P.items():
        lst_rouge_P.append(np.average(val, axis=0))
    for key, val in dic_rouge_R.items():
        lst_rouge_R.append(np.average(val, axis=0))
    for key, val in dic_rouge_F.items():
        lst_rouge_F.append(np.average(val, axis=0))
    return lst_rouge_R, lst_rouge_P, lst_rouge_F


def read_ROUGE_1(file_scores):
    return read_ROUGE(file_scores, 3)


def read_ROUGE_2(file_scores):
    return read_ROUGE(file_scores, 6)


def read_ROUGE_3(file_scores):
    return read_ROUGE(file_scores, 9)


def read_ROUGE_4(file_scores):
    return read_ROUGE(file_scores, 12)


def read_ROUGE_L(file_scores):
    return read_ROUGE(file_scores, 15)


def read_ROUGE_W(file_scores):
    return read_ROUGE(file_scores, 18)


def read_ROUGE_SU4(file_scores):
    return read_ROUGE(file_scores, 21)


def read_sera_results(sera_file):
    lst_results = []
    with open(sera_file, 'r') as file:
        for line in file:
            line = line.rstrip('\r\n').split()[-1]
            lst_results.append(float(line))
    return lst_results


def read_SERA_(file_scores, which_column):
    dic_sera = defaultdict(lambda: [])
    with open(file_scores, 'r') as file:
        for line in file:
            line = line.rstrip('\r\n').split()
            docs = line[0].split('.')[1]
            dic_sera[docs].append(float(line[which_column]))
    lst_values_sera = []
    for key, val in dic_sera.items():
            lst_values_sera.append(np.average(val, axis=0))
    return lst_values_sera


def read_SERA(file_scores, which_column):
    dic_sera = defaultdict(lambda: [])
    with open(file_scores, 'r') as file:
        for line in file:
            line = line.rstrip('\r\n').split()
            docs = line[0].split('.')[-1]
            dic_sera[docs].append(float(line[which_column]))
    lst_values_sera = []
    for key, val in dic_sera.items():
            lst_values_sera.append(np.average(val, axis=0))
    return lst_values_sera


def SERA_M1_M2_M3_M4(file_scores):
    return read_SERA(file_scores, 5)


def responsiveness(file_path):
    dic_resp = defaultdict(lambda: [])
    with open(file_path, 'r') as file:
        for line in file:
            line = line.rstrip('\r\n').split()
            docs = line[1]#.split('.')[1]
            # in line 8 we find the overall responsiveness judgment for the peer summary
            dic_resp[docs].append(float(line[8]) / 5)
    lst_values_responsiveness = []
    for key, val in dic_resp.items():
        lst_values_responsiveness.append(np.average(val, axis=0))
    return lst_values_responsiveness


def order_name_files(score_pyramid_file, sera_file, path_save_file):
    lst_name_sera, lst_score_sera = [], []
    with open(sera_file, 'r') as file_sera:
        for line in file_sera:
            line = line.rstrip('\r\n')

            name_score = line.split()
            score = name_score[-1]
            ID_name = name_score[0].split('.')[0]
            ID_number = name_score[0].split('.')[-1]
            final_name = ID_name + '.' + ID_number
            final_line = final_name + '\t' + score
            lst_name_sera.append(final_name)
            lst_score_sera.append(score)

    lst_orden_name_sera, lst_orden_score_sera = [], []
    with open (score_pyramid_file, 'r') as file_pyramid:
        for line in file_pyramid:
            line = line.rstrip('\r\n')
            ID_file = line.split()[0] # we get only the ID file

            if ID_file in lst_name_sera:
                index = lst_name_sera.index(ID_file)
                lst_orden_name_sera.append(ID_file)
                score_orden = lst_score_sera[index]
                lst_orden_score_sera.append(score_orden)

    for ID_sera, score_sera in zip( lst_orden_name_sera, lst_orden_score_sera):
        with open(path_save_file , 'a') as file:
            #line = ID_sera + '\t' + score_sera
            file.write(str(ID_sera) + '\t' + str(score_sera))
            file.write('\n')
            #print(ID_sera, score_sera)
            #print(line)



