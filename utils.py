#-*-coding:utf-8-*-

import os

def process_read(cntnt):
	return cntnt

def get_content(path_name_file_index, pool):
	with open(path_name_file_index, 'r', encoding='utf-8') as file_idx:
		results = pool.map(process_read, file_idx)
	return results

def read_cntnt(path_file):
	cntnt = ''
	with open(path_file, 'r', encoding='utf-8') as _file:
		for line in _file:
			line = line.rstrip('\r\n')
			cntnt = line + ' '
	return cntnt

def write_inf(name_file, dic_res):
	
	#with open(name_file, 'a+') as f_w:
	for key, val in dic_res.items():
		print(str(key) + val)
				#f_w.write(str(elem) + str(val) + '\n')

def write_score(name_file, dic_score):
	with open(name_file, 'w') as file:
		for key, val in dic_score.items():
			file.write(str(key) + '\t' + val + '\n')

def write_details(name_file, lst_details):
	cnt = 0
	with open(name_file, 'w') as file:
		for _dic in lst_details:
			cnt += 1
			for key, value in _dic.items():
				file.write(str(key) + '\t' + str(value))
				file.write('\n')
			if cnt % 5 == 0:
				file.write('\n')


def get_automatic_summaries_gold_standard(files_automatic_summaries, files_gold_standard):
	""" Goal: Read in correct way the automatic summaries and model summaries (gold standard or human summaries)
			  from TAC2008 dataset.
	"""
	dic_automatic_summaries = dict()
	ID_subset_automatic_summary = ''
	
	for path_automatic_summary in files_automatic_summaries:
		ID_number_summary		    = path_automatic_summary.split('/')[-1].split('.')[-1]
		
		if int(ID_number_summary) < 58:
			#ID_subset_automatic_summary = path_automatic_summary.split('/')[-1].split('.')[0]
			#ID_automatic_summary = ID_subset_automatic_summary + '.' + ID_number_summary
			dic_automatic_summaries[path_automatic_summary] = []


	for path_gold_standard in files_gold_standard:
		pattern_gold_standard = path_gold_standard.split('/')[-1].split('.')[0]

		for key, value in dic_automatic_summaries.items():
			if pattern_gold_standard in key:
				value.append(path_gold_standard)
				dic_automatic_summaries[key] = value

	return dic_automatic_summaries

def get_lst_candidate_files(file_path):
	lst_decoded_files = []
	with open(file_path, 'r') as file_cand:
		for line in file_cand:
			line = line.rstrip('\r\n')
			lst_decoded_files.append(line)
	return lst_decoded_files


def get_previous_state(name_file):
	dic_score = dict()
	if os.path.isfile(name_file):
		file = open(name_file, 'r')
		for line in file:
			key, val = line.split('\t')[0], line.split('\t')[-1]
			dic_score[key]=val
	return dic_score
