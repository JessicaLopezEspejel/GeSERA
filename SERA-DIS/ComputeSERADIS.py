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


import sys
import os
import glob
import argparse
from utils import read_file, write_file


def main():
    path_sera_dis = os.getcwd()
    path_sera_dis = '/'.join(path_sera_dis.split('/')[0:-1])
    # print(path_sera_dis)
    # sys.exit()
    parser = argparse.ArgumentParser()
    parser.add_argument('-path_sera_file', type=str, default=path_sera_dis+'/test/output/')
    parser.add_argument('-save_sera_dis', type=str, default=path_sera_dis+'/test/output/')

    opt = parser.parse_args()

    lst_scores = glob.glob(opt.path_sera_file + 'test_reference_vectors*')
    for score_file in lst_scores:
        file_name = score_file.split('/')[-1]
        path_save_file = opt.save_sera_dis + 'dis_score_' + file_name

        dic_results = read_file(score_file)
        write_file(path_save_file, dic_results)


if __name__ == '__main__':
    main()