#-*-coding:utf-8-*-
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
	
	def noun_verb_adjetive(self, parser, searcher, path_file, content_article, rank_cutpoint):
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
		
	def noun_verb_adjetive_adverb(self, parser, searcher, path_file, content_article, rank_cutpoint):
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
