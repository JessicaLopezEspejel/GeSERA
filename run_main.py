# -*- coding: utf-8 -*-

from __future__ import division
import glob
import sys
from whoosh.fields import Schema, TEXT
from whoosh.index import create_in, open_dir, exists_in
from whoosh.analysis import *
from whoosh import qparser
from whoosh.qparser import QueryParser
import time
import threading
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
import re
from nltk import sent_tokenize

from AnalyzersText import *
from QueryReformulation import *
from MeasureSera import *
from utils import *


general_path = '/scratch_ssd/jessica/TAC2008_AQUAINT-2/' 

path_index    = general_path + 'index/'
indexdir      = general_path + 'index_balanced_15mil/txt/'

decoded_dir   = general_path + 'lst_files_evaluation.txt'
reference_dir = general_path + 'queries/models/'
dir_results   = general_path + 'results_balanced_15mil/'

lst_articlesIndex_files =  glob.glob(indexdir+"*.txt")#[0:20]#[0:11400] #[0:11400] # 242,703
lst_reference_files 	=  sorted(glob.glob(reference_dir+"D08*")) # total: 10,699 sorted()
#lst_decoded_files   	=  sorted(glob.glob(decoded_dir+"D08*"))   # total: 10,699
lst_decoded_files 	=  get_lst_candidate_files(decoded_dir)

class SERA():
		
	def __init__(self):
		pass

	def main():	

		# python v1.py 1 1 5 "hola" 200 50000
		write_chunk = 6


		total_summaries = len(lst_decoded_files)
		print('*'*10 + ' Found {} query summaries '.format(total_summaries) + '*'*10)

		if sys.argv[3] == '5': 
			rank_cutpoint = 5
		if sys.argv[3] == '10': 
			rank_cutpoint = 10
		else: 
			rank_cutpoint = 5

		name_index 	= sys.argv[4]
		input_interval = [0, total_summaries]
		tab = sys.argv[5].split("-")
		if len(tab)==2:
			input_interval = [ int(tab[0]) ,int(tab[1]) ]
		else:
			input_interval = [ 0, int(sys.argv[5]) ]
		num_docs_index 	= int(sys.argv[6])
		start_over = False
		if len(sys.argv) > 7: 
			start_over = sys.argv[7] in ['1','yes','true']

		# Objects
		dic_automatic_summaries = get_automatic_summaries_gold_standard(lst_decoded_files[input_interval[0]:input_interval[1]], lst_reference_files)
		analyzersText = AnalyzersText()
		sqr  = QueryReformulation()
		pool = Pool(8)
		poolq = ThreadPool(processes=2)
		
		num_files = len(dic_automatic_summaries)

		#lst_articlesIndex_random_files = analyzersText.random_files_index(lst_articlesIndex_files, num_docs_index)
		lst_articlesIndex_random_files = lst_articlesIndex_files[0:num_docs_index]
		lst_reference_random_files = lst_reference_files[input_interval[0]:input_interval[1]]
		lst_decoded_random_files   = lst_decoded_files[input_interval[0]:input_interval[1]]
		

		schema = Schema( path=TEXT(stored=True) , content=TEXT(analyzer=StemmingAnalyzer()) ) # content=TEXT(analyzer=StemmingAnalyzer()), RegexTokenizer() 
		t0 = time.time()
		if not exists_in(path_index, name_index):
			print('*'*10 + ' Building the index for {} documents '.format(num_docs_index) + '*'*10)
			ix = create_in(path_index, schema, name_index) # return an index.
			writer = ix.writer(procs=6, multisegment=True, limitmb=4096) # procs=6, limitmb=4GB## OR 8192
			
			for  idx, path_name_file_index in enumerate(lst_articlesIndex_random_files):
				if idx % 10000 == 0:
					t1 = time.time()
					print("  {}/{}. elapsed time : {}s".format(idx,num_docs_index, round(t1-t0,3) ))
				
				article_cntnt = get_content(path_name_file_index, pool)
				article_cntnt = " ".join(article_cntnt)
				
				#if sys.argv[2] == '1':
				#	article_cntnt = article_cntnt
				#if sys.argv[2] == '2':
				#	article_cntnt = analyzersText.get_chunk_NP(article_cntnt)
				#if sys.argv[2] == '3':
				#	article_cntnt = sqr.get_keywords(sent_tokenize(article_cntnt))
				#if sys.argv[2] == '4':
				#	article_cntnt = analyzersText.get_noun_verb_adjetive(article_cntnt)
				#if sys.argv[2] == '5':
				#	article_cntnt = analyzersText.get_noun_verb_adjetive_adverb(article_cntnt)
				
				#article_cntnt_uni = article_cntnt.decode('utf-8')
				writer.add_document(path=path_name_file_index, content=article_cntnt) # , time=modtime
				""" Con la instruccion: writer.remove_field("path") 
				    borra el path y entonces tenemos que volver a crear el indice con la
				"""
				#writer.remove_field("path")

			writer.commit(merge=False) # commit all at once. Merge is to prevent Whoosh merges segments during commit.
	
			t1 = time.time()
			print('*'*10 + ' Index built in {}s '.format(round(t1-t0,3)) + '*'*10) # It's CPU seconds elapsed (floating point)

		ix = open_dir(path_index, name_index)
		
		# **********************************************************************************************************************#
		# Parse a query string

		sera = MeasureSera()
		num_file, sum_sera, sum_dis_sera = 0, 0, 0
		dic_res, dic_score = dict(), dict()
		lst_details = []
		name_file = dir_results + name_index + ".txt"
		name_f_scores = dir_results + 'score_' + name_index + '_' + '-'.join([str(i) for i in input_interval])  + '.txt'
		name_details =  dir_results + name_index + '_' + '-'.join([str(i) for i in input_interval])  + '.txt'


		if not start_over:
			dic_score = get_previous_state(name_f_scores)

		searcher = ix.searcher()
		parser = QueryParser("content", schema=schema, group=qparser.OrGroup) #ix.schema
		
		lst_scores_reference = []
		num_summaries = input_interval[1]-input_interval[0]
		print('*'*10 + ' Processing {} summary queries : {}->{} '.format(num_summaries,input_interval[0],input_interval[1]) + '*'*10)
		t0 = time.time()
		for path_candidate, lst_manual_summaries in dic_automatic_summaries.items(): # Candidate summary
			print('.'*10, path_candidate)
					
			num_file+= 1
			try:
				cntnt_cand = get_content(path_candidate, pool)[0]
			except Exception as error:
				cntnt_cand = " "
			
			nom_file = path_candidate.split('/')[-1]
			cad_scores = ''

			if nom_file in dic_score:
				continue

			if sys.argv[2] == '1': # Text without stop words and without numeric values
				dic_cand = poolq.apply_async(sqr.raw_text, args=(parser, searcher, path_candidate, cntnt_cand, rank_cutpoint))
			if sys.argv[2] == '2': # Noun Phrases
				dic_cand = poolq.apply_async(sqr.noun_phrases, args=(parser, searcher, path_candidate, cntnt_cand, rank_cutpoint))
			if sys.argv[2] == '3': # Keywords
				dic_cand = poolq.apply_async(sqr.keywords, args=(parser, searcher, path_candidate, cntnt_cand, rank_cutpoint))
			if sys.argv[2] == '4': # Noun phrases, 	verb, adjetive
				dic_cand = poolq.apply_async(sqr.noun_verb_adjetive, args=(parser, searcher, path_candidate, cntnt_cand, rank_cutpoint))
			if sys.argv[2] == '5':
				dic_cand = poolq.apply_async(sqr.noun_verb_adjetive_adverb, args=(parser, searcher, path_candidate, cntnt_cand, rank_cutpoint))
			dic_candidate = dic_cand.get()
			
			lst_details.append(dic_candidate)

			for path_reference in lst_manual_summaries: # Reference summaries
				
				avg_dis_sera, avg_sera = 0, 0
				try:
					cntnt_ref = get_content(path_reference, pool)[0]
				except Exception as error:
					cntnt_ref = " "

				# Type of text
				if sys.argv[2] == '1': # Text without stop words and without numeric values
					dic_ref = poolq.apply_async(sqr.raw_text, args=(parser, searcher, path_reference, cntnt_ref, rank_cutpoint))
				if sys.argv[2] == '2': # Noun Phrases
					dic_ref = poolq.apply_async(sqr.noun_phrases, args=(parser, searcher, path_reference, cntnt_ref, rank_cutpoint))
				if sys.argv[2] == '3': # Keywords
					dic_ref = poolq.apply_async(sqr.keywords, args=(parser, searcher, path_reference, cntnt_ref, rank_cutpoint))
				if sys.argv[2] == '4': # noun phrases, verb, adjetive
					dic_ref = poolq.apply_async(sqr.noun_verb_adjetive, args=(parser, searcher, path_reference, cntnt_ref, rank_cutpoint))
				if sys.argv[2] == '5':
					dic_ref = poolq.apply_async(sqr.noun_verb_adjetive_adverb, args=(parser, searcher, path_reference, cntnt_ref, rank_cutpoint))
				dic_reference = dic_ref.get()

				lst_details.append(dic_reference)

				# Type of SERA
				if sys.argv[1] == '1': # SERA
					file_num, score_sera = sera.sera_int(dic_reference, dic_candidate, rank_cutpoint)
					sum_sera += score_sera 
					avg_sera = sum_sera / num_file
					cad_scores += str(score_sera) + ' '

				if sys.argv[1] == '2':
					#print('dic_candidate: ', dic_candidate)
					#print('dic_reference: ', dic_reference)
					file_num, score_dis_sera = sera.dis_sera(dic_reference, dic_candidate)
					sum_dis_sera += score_dis_sera
					avg_dis_sera = sum_dis_sera / num_file
					#dic_res[file_num] = [dic_reference, dic_candidate, (file_num, score_dis_sera, avg_dis_sera)]
					cad_scores += str(score_dis_sera) + ' '


			dic_score[nom_file] = cad_scores
			
			if num_file % write_chunk == 0 or num_file == num_files:
				t1 = time.time()
				print("  {}/{}. elapsed time : {}s".format(num_file,num_files, round(t1-t0,3) ))
				writer_score = threading.Thread(target=write_score, args=(name_f_scores, dic_score))
				writer_score.start()
				writer_details = threading.Thread(target=write_details, args=(name_details, lst_details))
				writer_details.start()


		searcher.close()

		t1 = time.time()
		print('*'*10 + ' Evaluation done in {}s '.format(round(t1-t0,3) ) + '*'*10)

	if __name__=="__main__":
		main()
