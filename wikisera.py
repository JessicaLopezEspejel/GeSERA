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
import sys
import shutil
import os
import glob
import datetime
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
	parser.add_argument('-x', type=str, default='wiki')  # index name
	parser.add_argument('-d', type=str, default=path_wikisera + '/data/wiki10000/')  # documents to index
	parser.add_argument('-s', type=str, default=path_wikisera + '/data/index/')  # save index folder

	opt = parser.parse_args()
	opt.o = opt.o + "/"
	if not os.path.isdir(opt.o):
		os.makedirs(opt.o)
	if not os.path.isdir(opt.s):
		os.makedirs(opt.s)

	lst_index_files = glob.glob(opt.d + "/*")
	lst_reference_files = sorted(glob.glob(opt.r + "/*"))

	if os.path.isdir(opt.c):
		lst_decoded_files = sorted(glob.glob(opt.c + "/*"))
	else:
		lst_decoded_files = [e.strip() for e in open(opt.c, 'r').readlines()]

	write_chunk = 6

	total_summaries = len(lst_decoded_files)
	print('*' * 10 + ' Found {} query summaries '.format(total_summaries) + '*' * 10)

	if opt.p != 5 and opt.p != 10:
		print("The value of the rank cut point should be 5 or 10")

	input_interval = [0, 0]
	if opt.i is None:
		opt.i = '0-' + str(len(lst_decoded_files))
		input_interval = get_interval(opt.i)
	else:
		input_interval = get_interval(opt.i)
	print('Interval of summaries to evaluate:', opt.i)

	# Objects
	dic_automatic_summaries = get_automatic_summaries_gold_standard(
		lst_decoded_files[input_interval[0]:input_interval[1]], lst_reference_files)
	num_files = len(dic_automatic_summaries)

	lst_doc_index = lst_index_files[0:opt.n]
	print("Using a ", len(lst_doc_index), " Wikipedia documents index")
	timestamp = "." + datetime.datetime.now().strftime('%Y.%m.%d.%Hh%M')
	
	pool = Pool(8)
	schema = Schema(path=TEXT(stored=True), content=TEXT(analyzer=StemmingAnalyzer()))
	
	ix = create_index(opt.s, opt.x, opt.n, lst_doc_index, schema, pool)

	# Parse a query string
	sera = MeasureSera()

	name_f_scores = opt.o + 'score_' + opt.t + '_' + opt.q + '_' + str(opt.p) + '_' + '-'.join(
		[str(i) for i in input_interval]) + timestamp + '.txt'
	
	name_details = opt.o + opt.t + '_' + opt.q + '_' + str(opt.p) + '_' + '-'.join(
		[str(i) for i in input_interval]) + timestamp + '.txt'

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
