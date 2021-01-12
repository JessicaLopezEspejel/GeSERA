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

from AnalyzersText import *
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import sent_tokenize


class QueryReformulation:

	def __init__(self):
		self.analyzersText = AnalyzersText()

	def get_keywords(self, lst_sentences):
		try:
			vectorizer = TfidfVectorizer(ngram_range=(1, 3))
			X = vectorizer.fit_transform(lst_sentences)
			lst_n_grams = vectorizer.get_feature_names()
		except Exception as error:
			lst_n_grams = lst_sentences
		return ' '.join(lst_n_grams)

	def keywords(self, parser, searcher, path_file, cntnt_article, rank_cutpoint):
		dic_results = dict()
		number_file = self.analyzersText.get_number_from_name_file(path_file) # we get something like 000000
		lst_sentences = sent_tokenize(cntnt_article)
		cntnt = self.get_keywords(lst_sentences)
		myquery = parser.parse(cntnt)
		results = searcher.search(myquery, limit= rank_cutpoint)

		docs = ()
		for x in list(results):
			doc_name = x['path'].split('/')[-1][:-4]
			docs += (doc_name,)
		dic_results[number_file] = docs
		return dic_results

	def raw_text(self, parser, searcher, path_file, cntnt_article, rank_cutpoint):
		dic_results = dict()
		number_file = self.analyzersText.get_number_from_name_file(path_file) # we get something like 000000
		myquery = parser.parse(cntnt_article)
		results = searcher.search(myquery, limit= rank_cutpoint)

		docs = ()
		for x in list(results):
			doc_name = x['path'].split('/')[-1][:-4]
			docs += (doc_name,)
		dic_results[number_file] = docs
		return dic_results

	def noun_phrases(self, parser, searcher, path_file, cntnt_article, rank_cutpoint):
		dic_results = dict()
		number_file = self.analyzersText.get_number_from_name_file(path_file) # we get something like 000000
		query_text = self.analyzersText.get_chunk_NP(cntnt_article)
		myquery = parser.parse(query_text)
		results = searcher.search(myquery, limit= rank_cutpoint)
		
		docs = ()
		for x in list(results):
			doc_name = x['path'].split('/')[-1][:-4]
			docs += (doc_name,)
		dic_results[number_file] = docs
		return dic_results
	
	def noun_verb_adjective(self, parser, searcher, path_file, content_article, rank_cutpoint):
		dic_results = dict()
		number_file = self.analyzersText.get_number_from_name_file(path_file) # we get something like 000000	
		query_text = self.analyzersText.get_noun_verb_adjetive(content_article)
		myquery = parser.parse(query_text)
		results = searcher.search(myquery, limit= rank_cutpoint)

		docs = ()
		for x in list(results):
			doc_name = x['path'].split('/')[-1][:-4]
			docs += (doc_name,)
		dic_results[number_file] = docs
		return dic_results
		
	def noun_verb_adjective_adverb(self, parser, searcher, path_file, content_article, rank_cutpoint):
		dic_results = dict()
		number_file = self.analyzersText.get_number_from_name_file(path_file) # we get something like 000000
		query_text = self.analyzersText.get_noun_verb_adjetive_adverb(content_article)
		myquery = parser.parse(query_text)
		results = searcher.search(myquery, limit= rank_cutpoint)

		docs = ()
		for x in list(results):
				doc_name = x['path'].split('/')[-1][:-4]
				docs += (doc_name,)
		dic_results[number_file] = docs
		return dic_results
