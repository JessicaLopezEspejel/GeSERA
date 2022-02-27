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
import time
from whoosh.index import create_in, open_dir, exists_in

from utils import get_content


def create_index(save_index_folder, index_name, num_docs_index, lst_articlesIndex_random_files, schema, pool):
    t0 = time.time()
    if not exists_in(save_index_folder, index_name):
        print('*' * 10 + ' Building the index for {} documents '.format(num_docs_index) + '*' * 10)
        ix = create_in(save_index_folder, schema, index_name)  # it returns an index.
        writer = ix.writer(procs=6, multisegment=True, limitmb=4096)  # procs=6, limitmb=4GB## OR 8192

        for idx, path_name_file_index in enumerate(lst_articlesIndex_random_files):
            if idx % 10000 == 0:
                t1 = time.time()
                print("  {}/{}. elapsed time : {}s".format(idx, num_docs_index, round(t1 - t0, 3)));
                sys.stdout.flush()

            article_cntnt = get_content(path_name_file_index, pool)
            article_cntnt = " ".join(article_cntnt)

            writer.add_document(path=path_name_file_index, content=article_cntnt)  # , time=modtime
        # writer.remove_field("path")
        writer.commit(merge=False)
        t1 = time.time()
        print('*' * 10 + ' Index built in {}s '.format(round(t1 - t0, 3)) + '*' * 10)  # It's CPU seconds elapsed (floating point)

    ix = open_dir(save_index_folder, index_name)

    return ix