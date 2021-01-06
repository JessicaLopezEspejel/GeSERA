# -*- coding: utf-8 -*-

from __future__ import division
import sys
import glob
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, open_dir, exists_in
from whoosh.analysis import *
from whoosh import qparser
from whoosh.qparser import QueryParser
import time
import threading
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import argparse

from QueryReformulation import *
from MeasureSera import *
from utils import *


# python /home/jessica/codes/TAC2008_SERA_BIEN/run.py
# -index_docs_folder /scratch_ssd/jessica/TAC2008_AQUAINT-2/index_balanced_60mil/txt/
# -save_index_folder /scratch_ssd/jessica/TAC2008_AQUAINT-2/index_60mil/
# -reference_folder /scratch_ssd/jessica/TAC2008_AQUAINT-2/queries/models/
# -candidate_folder  /scratch_ssd/jessica/TAC2008_AQUAINT-2/queries/candidates/
# -results_folder /scratch_ssd/jessica/TAC2008_AQUAINT-2/results_balanced_60mil/
# -index_name "test" -cut_off_point 5 -interval 0-2 -num_docs_index 60000
# -refine_query raw -sera_type dis


'''
python /home/jessica/codes/SERA-plus/run.py \
-index_docs_folder  /scratch_global/jessica/datasets/DUC2007/my_dataset/preprocessed/index_DUC2007/txt/ \
-save_index_folder /scratch_global/jessica/datasets/DUC2007/my_dataset/preprocessed/index/SERA_1_5/ \
-reference_folder /scratch_global/jessica/datasets/DUC2007/my_dataset/preprocessed/queries/models/  \
-candidate_folder /scratch_global/jessica/datasets/DUC2007/my_dataset/preprocessed/queries/candidates/  \
-results_folder /scratch_global/jessica/datasets/DUC2007/my_dataset/preprocessed/results/ \
-refine_query raw \
-cut_off_point 5 -num_docs_index 1125  -index_name SERA_1_5 -interval 0-1440

'''
def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-index_docs_folder', type=str, default='')  # folder you can find the files you will index
	parser.add_argument('-save_index_folder', type=str, default='')  # save you will save the index
	parser.add_argument('-txt_decoder_files', type=str, default='')  # txt where there is a list of summaries you want to evaluate
	parser.add_argument('-reference_folder', type=str, default='')  # folder where there are the reference files
	parser.add_argument('-candidate_folder', type=str, default='')  # it's the folder where there are the candidate docs
	parser.add_argument('-results_folder', type=str, default='')  # the folder will save your results
	parser.add_argument('-index_name', type=str, default='')
	parser.add_argument('-cut_off_point', type=int, default=5)
	parser.add_argument('-interval', type=str, default='0-2')
	parser.add_argument('-num_docs_index', type=int, default=10000)
	parser.add_argument('-refine_query', type=str, default='raw')
	parser.add_argument('-sera_type', type=str, default='sera')  #sera or dis

	opt = parser.parse_args()

	if not os.path.isdir(opt.results_folder):
		os.makedirs(opt.results_folder)
	if not os.path.isdir(opt.save_index_folder):
		os.makedirs(opt.save_index_folder)

	lst_articlesIndex_files = glob.glob(opt.index_docs_folder + "*")
	lst_reference_files = sorted(glob.glob(opt.reference_folder + "D08*"))
	if os.path.isdir(opt.candidate_folder):
		lst_decoded_files = sorted(glob.glob(opt.candidate_folder + "D08*"))
	else:
		lst_decoded_files = [e.strip() for e in open(opt.candidate_folder, 'r').readlines()]

	# print(lst_decoded_files)
	# sys.exit()


	write_chunk = 6

	total_summaries = len(lst_decoded_files)
	print('*' * 10 + ' Found {} query summaries '.format(total_summaries) + '*' * 10)

	if opt.cut_off_point != 5 and opt.cut_off_point != 10:
		print("The value of the rank cut point should be 5 or 10")

	input_interval = [0, total_summaries]

	tab = opt.interval.split('-')

	if len(tab) == 2:
		input_interval = [int(tab[0]), int(tab[1])]
	else:
		input_interval = [0, int(opt.interval)]
	# Objects
	dic_automatic_summaries = get_automatic_summaries_gold_standard(
		lst_decoded_files[input_interval[0]:input_interval[1]], lst_reference_files)

	print("dic_automatic_summaries: ", len(dic_automatic_summaries))

	sqr = QueryReformulation()
	pool = Pool(8)
	poolq = ThreadPool(processes=2)

	num_files = len(dic_automatic_summaries)
	lst_articlesIndex_random_files = lst_articlesIndex_files[0:opt.num_docs_index]
	print("lst_articlesIndex_random_files", len(lst_articlesIndex_random_files))

	lst_reference_random_files = lst_reference_files[input_interval[0]:input_interval[1]]
	lst_decoded_random_files = lst_decoded_files[input_interval[0]:input_interval[1]]

	schema = Schema(path=TEXT(stored=True), content=TEXT(
		analyzer=StemmingAnalyzer()))  # content=TEXT(analyzer=StemmingAnalyzer()), RegexTokenizer()
	t0 = time.time()
	if not exists_in(opt.save_index_folder, opt.index_name):
		print('*' * 10 + ' Building the index for {} documents '.format(opt.num_docs_index) + '*' * 10)
		ix = create_in(opt.save_index_folder, schema, opt.index_name)  # it returns an index.
		writer = ix.writer(procs=6, multisegment=True, limitmb=4096)  # procs=6, limitmb=4GB## OR 8192

		for idx, path_name_file_index in enumerate(lst_articlesIndex_random_files):
			if idx % 10000 == 0:
				t1 = time.time()
				print("  {}/{}. elapsed time : {}s".format(idx, opt.num_docs_index, round(t1 - t0, 3))) ; sys.stdout.flush()

			article_cntnt = get_content(path_name_file_index, pool)
			article_cntnt = " ".join(article_cntnt)

			writer.add_document(path=path_name_file_index, content=article_cntnt)  # , time=modtime
		# writer.remove_field("path")
		writer.commit(merge=False)
		t1 = time.time()
		print('*' * 10 + ' Index built in {}s '.format(
			round(t1 - t0, 3)) + '*' * 10)  # It's CPU seconds elapsed (floating point)

	ix = open_dir(opt.save_index_folder, opt.index_name)

	# **************************************************************************************************************
	# Parse a query string

	sera = MeasureSera()
	num_file, sum_sera, sum_dis_sera = 0, 0, 0
	dic_res, dic_score = dict(), dict()
	lst_details = []
	name_file = opt.results_folder + opt.index_name + ".txt"
	name_f_scores = opt.results_folder + 'score_' + opt.index_name + '_' + '-'.join(
		[str(i) for i in input_interval]) + '.txt'
	name_details = opt.results_folder + opt.index_name + '_' + '-'.join([str(i) for i in input_interval]) + '.txt'


	searcher = ix.searcher()
	parser_query = QueryParser("content", schema=schema, group=qparser.OrGroup)  # ix.schema

	num_summaries = input_interval[1] - input_interval[0]
	print('*' * 10 + ' Processing {} summary queries : {}->{} '.format(num_summaries, input_interval[0],
																	   input_interval[1]) + '*' * 10)
	t0 = time.time()
	for path_candidate, lst_manual_summaries in dic_automatic_summaries.items():  # Candidate summary
		print('.' * 10, path_candidate)

		num_file += 1
		try:
			cntnt_cand = get_content(path_candidate, pool)[0]
		except Exception as error:
			cntnt_cand = " "

		nom_file = path_candidate.split('/')[-1]
		cad_scores = ''

		if nom_file in dic_score:
			continue

		if  'raw' in opt.refine_query:  # Text without stop words and without numeric values
			dic_cand = poolq.apply_async(sqr.raw_text,
										 args=(parser_query, searcher, path_candidate, cntnt_cand, opt.cut_off_point))
		if 'np' in opt.refine_query:   # Noun Phrases
			dic_cand = poolq.apply_async(sqr.noun_phrases,
										 args=(parser_query, searcher, path_candidate, cntnt_cand, opt.cut_off_point))
		if 'kw' in opt.refine_query:  # Keywords
			dic_cand = poolq.apply_async(sqr.keywords,
										 args=(parser_query, searcher, path_candidate, cntnt_cand, opt.cut_off_point))
		if 'plus' in opt.refine_query:  # Noun phrases, verb, adjective
			dic_cand = poolq.apply_async(sqr.noun_verb_adjetive,
										 args=(parser_query, searcher, path_candidate, cntnt_cand, opt.cut_off_point))
		dic_candidate = dic_cand.get()

		lst_details.append(dic_candidate)

		for path_reference in lst_manual_summaries:  # Reference summaries

			avg_dis_sera, avg_sera = 0, 0
			try:
				cntnt_ref = get_content(path_reference, pool)[0]
			except Exception as error:
				cntnt_ref = " "

			# Type of text
			if 'raw' in opt.refine_query:  # Text without stop words and without numeric values
				dic_ref = poolq.apply_async(sqr.raw_text,
											args=(parser_query, searcher, path_reference, cntnt_ref, opt.cut_off_point))
			if 'np' in opt.refine_query:  # Noun Phrases
				dic_ref = poolq.apply_async(sqr.noun_phrases,
											args=(parser_query, searcher, path_reference, cntnt_ref, opt.cut_off_point))
			if 'kw' in opt.refine_query:  # Keywords
				dic_ref = poolq.apply_async(sqr.keywords,
											args=(parser_query, searcher, path_reference, cntnt_ref, opt.cut_off_point))
			if 'plus' in opt.refine_query:  # noun phrases, verb, adjetive
				dic_ref = poolq.apply_async(sqr.noun_verb_adjetive,
											args=(parser_query, searcher, path_reference, cntnt_ref, opt.cut_off_point))
			dic_reference = dic_ref.get()

			lst_details.append(dic_reference)

			# Type of SERA
			if 'sera' in opt.sera_type:
				file_num, score_sera = sera.sera_int(dic_reference, dic_candidate, opt.cut_off_point)
				sum_sera += score_sera
				avg_sera = sum_sera / num_file
				cad_scores += str(score_sera) + ' '

			if 'dis' in opt.sera_type:
				file_num, score_dis_sera = sera.dis_sera(dic_reference, dic_candidate)
				sum_dis_sera += score_dis_sera
				avg_dis_sera = sum_dis_sera / num_file
				cad_scores += str(score_dis_sera) + ' '

		dic_score[nom_file] = cad_scores

		if num_file % write_chunk == 0 or num_file == num_files:
			t1 = time.time()
			print("  {}/{}. elapsed time : {}s".format(num_file, num_files, round(t1 - t0, 3)))
			writer_score = threading.Thread(target=write_score, args=(name_f_scores, dic_score))
			writer_score.start()
			writer_details = threading.Thread(target=write_details, args=(name_details, lst_details))
			writer_details.start()

	searcher.close()

	t1 = time.time()
	print('*' * 10 + ' Evaluation done in {}s '.format(round(t1 - t0, 3)) + '*' * 10)


if __name__ == '__main__':
	main()
