#-*-coding:utf-8-*-

from whoosh.analysis import RegexTokenizer
from whoosh.analysis import LowercaseFilter
from whoosh.analysis import StopFilter
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
import spacy
import random


import en_core_web_sm



class AnalyzersText():

	def __init__(self):
		pass 

	global bad_chars
	global stop_words
	global sp
	global nlp

	# nlp = spacy.load("en_core_web_sm")
	nlp = en_core_web_sm.load()


	bad_chars = [',', '¿', '?', '(', ')', '[', ']', '"', '\\', '€', '£', '$','»', '%', '°', '@', '/',
					 ';', ':', '«', '“',  '·', '¡', '!', '#', '&', '=','_', '-', '|', '{', '}', '`', '+', '*',
					 '%', '±', 'μ', '<', '>', '≤', '≥', '¬', '~', '½', '¢', 'ł','ĸ', 'ħ', 'ŋ', 'đ', 'ð', 'ß',
					 'æ','@', 'ł', '¶', 'ŧ', '←', '↓', '→', 'ø', 'þ', '^', '√'] # miss dot (.) # 65 characters.

	stop_words = set(stopwords.words('english'))
	sp = spacy.load('en_core_web_sm')

	def random_files_index(self, lst_files, limit_files):
		dic_files = dict()
		while len(dic_files) < limit_files:
			rnd_number = random.randrange(0,len(lst_files))
			dic_files[rnd_number] = lst_files[rnd_number]
		return list(dic_files.values())

	def random_file_summaries(self, lst_standar_goal, lst_summaries_generated, limit_files):
		dic_goal = dict()
		dic_summaries = dict()

		while len(dic_goal) < limit_files:
			rnd_number = random.randrange(0,len(lst_standar_goal))
			dic_goal[rnd_number] = lst_standar_goal[rnd_number]
			dic_summaries[rnd_number] = lst_summaries_generated[rnd_number]
		return list(dic_goal.values()), list(dic_summaries.values())

	def get_number_from_name_file(self, path_file):
		return path_file.split('/')[-1].split('_')[0]

	def is_number(self, s):
		try:
			float(s)
			return True
		except ValueError:
			return False

	def clean_up(self, str_text):
		"""
		Input: string text.
		Goal: Lower case, tokenization word by word, remove stop words, remove typography and remove numbers.
		Lemmatization.
		Output: String text.
		"""
		str_final = ''
		str_text = str_text.lower()
		str_clean = ''
		for sent in sent_tokenize(str_text):
			sentence = sp(sent)
			for token in sentence:
				if token.text not in bad_chars and  self.is_number(token.text) == False and token.text not in stop_words:
					token = token.lemma_
					str_clean += token +' '
		return str_clean

	def get_chunk_NP(self, txt):
		doc = nlp(txt)
		str_chunk = ''
		for chunk in doc.noun_chunks:
			str_chunk += chunk.text + " "
		return str_chunk
	
	def get_noun_verb_adjetive(self, txt):
		lst_words = []
		lst_noun_verb_adj = pos_tag(word_tokenize(txt))

		for token, token_type in lst_noun_verb_adj:
			if token_type == 'NN' or token_type == 'NNS':  # or token_type == 'NNP' or token_type == 'NNPS':
				lst_words.append(token)
			if token_type =='VB' or token_type =='VBP' or token_type =='VBG' or token_type == 'VBD' or token_type =='VBN' or token_type =='VBZ':
				lst_words.append(token)
			if token_type == 'JJ' or token_type == 'JJR' or token_type == 'JJS':
				lst_words.append(token)
		return ' '.join(lst_words)

	def get_noun_verb_adjetive_adverb(self, txt):
		lst_words = []
		lst_noun_verb_adj = pos_tag(word_tokenize(txt))
		
		for token, token_type in lst_noun_verb_adj:
			if token_type == 'NN' or token_type == 'NNS' or token_type == 'NNP' or token_type == 'NNPS':
				lst_words.append(token)
			if token_type =='VB' or token_type == 'VBD' or token_type =='VBG' or token_type =='VBN' or token_type =='VBZ':
				lst_words.append(token)
			if token_type == 'JJ' or token_type == 'JJR' or token_type == 'JJS':
				lst_words.append(token)
			if token_type == 'RB' or token_type == 'RBR' or token_type == 'RBS':
				lst_words.append(token)
		return ' '.join(lst_words)
