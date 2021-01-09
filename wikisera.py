# -*- coding: utf-8 -*-

from __future__ import division
import sys
import os
import glob
from whoosh.fields import Schema, TEXT
from whoosh.analysis import *
from whoosh import qparser
from whoosh.qparser import QueryParser
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import argparse

from QueryReformulation import *
from MeasureSera import *
from utils import *
from index import create_index
from menu import display_menu


def main():
	path_wikisera = os.getcwd()
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', type=str, default='')  # candidate documents folder
	parser.add_argument('-r', type=str, default='')  # reference documents folder
	parser.add_argument('-o', type=str, default='')  # the folder will save your results
	parser.add_argument('-q', type=str, default='raw')  # refine_query
	parser.add_argument('-t', type=str, default='sera')  # sera_type: sera or dis
	parser.add_argument('-n', type=int, default=10000)  # num_docs_index
	parser.add_argument('-i', type=str, default=None)  # interval
	parser.add_argument('-p', type=int, default=5)  # cut_off_point
	parser.add_argument('-index_name', type=str, default='wiki')  # index name
	parser.add_argument('-index_docs_folder', type=str, default=path_wikisera + '/data/wiki30000/')  # files to index
	parser.add_argument('-save_index_folder', type=str, default=path_wikisera + '/data/index/')  # save index

	opt = parser.parse_args()

	if not os.path.isdir(opt.o):
		os.makedirs(opt.o)
	if not os.path.isdir(opt.save_index_folder):
		os.makedirs(opt.save_index_folder)

	lst_index_files = glob.glob(opt.index_docs_folder + "*")
	lst_reference_files = sorted(glob.glob(opt.r + "*"))

	if os.path.isdir(opt.c):
		lst_decoded_files = sorted(glob.glob(opt.c + "*"))
	else:
		lst_decoded_files = [e.strip() for e in open(opt.c, 'r').readlines()]

	write_chunk = 6

	total_summaries = len(lst_decoded_files)
	print('*' * 10 + ' Found {} query summaries '.format(total_summaries) + '*' * 10)

	if opt.p != 5 and opt.p != 10:
		print("The value of the rank cut point should be 5 or 10")

	input_interval = [0, 0]
	if opt.i is None:
		opt.i = len(lst_decoded_files)
	else:
		input_interval = get_interval(opt.i)
	print('Interval of summaries to evaluate:', opt.i)

	# Objects
	dic_automatic_summaries = get_automatic_summaries_gold_standard(
		lst_decoded_files[input_interval[0]:input_interval[1]], lst_reference_files)
	num_files = len(dic_automatic_summaries)

	lst_doc_index = lst_index_files[0:opt.n]
	print("lst_doc_index", len(lst_doc_index))
	# lst_reference_random_files = lst_reference_files[input_interval[0]:input_interval[1]]
	# lst_decoded_random_files = lst_decoded_files[input_interval[0]:input_interval[1]]

	pool = Pool(8)
	schema = Schema(path=TEXT(stored=True), content=TEXT(analyzer=StemmingAnalyzer()))
	# content=TEXT(analyzer=StemmingAnalyzer()), RegexTokenizer()
	ix = create_index(opt.save_index_folder, opt.index_name, opt.n, lst_doc_index, schema, pool)

	# Parse a query string
	sera = MeasureSera()

	name_f_scores = opt.o + 'score_' + opt.index_name + '_' + '-'.join(
		[str(i) for i in input_interval]) + '.txt'
	name_details = opt.o + opt.index_name + '_' + '-'.join([str(i) for i in input_interval]) + '.txt'

	sqr = QueryReformulation()
	searcher = ix.searcher()
	parser_query = QueryParser("content", schema=schema, group=qparser.OrGroup)  # ix.schema
	num_summaries = input_interval[1] - input_interval[0]

	print('*' * 10 + ' Processing {} summary queries : {}->{} '.format(num_summaries, input_interval[0],
																	   input_interval[1]) + '*' * 10)
	t0 = time.time()
	pool_thread = ThreadPool(processes=2)

	display_menu(opt.q, opt.p, sera, opt.t, pool_thread, sqr, pool, searcher,
				parser_query, dic_automatic_summaries, num_files, name_f_scores, name_details, write_chunk, t0)

	searcher.close()

	t1 = time.time()
	print('*' * 10 + ' Evaluation done in {}s '.format(round(t1 - t0, 3)) + '*' * 10)


if __name__ == '__main__':
	main()