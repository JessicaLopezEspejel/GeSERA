
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