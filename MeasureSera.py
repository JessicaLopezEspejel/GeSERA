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
from math import log, fabs


class MeasureSera():

	def __init__(self):
		pass

	def sera_int(self, dic_results_candidate, dic_results_reference, cutoff_point):
		number_candidate = ''
		intersection_res = 0
		for (number_cand, result_cand),(number_ref, result_ref) in zip(dic_results_candidate.items(), dic_results_reference.items()):
			number_candidate = number_cand
			intersection_res = len(set(result_cand).intersection(set(result_ref)))
		score = intersection_res / cutoff_point

		return number_candidate, score

	def dis_sera(self, dic_results_candidate, dic_results_reference):
		
		number_candidate = ''
		div, D_max = 0, 0

		lst_candidate, lst_reference = [], []
		for (num_cand, result_cand), (num_ref, result_ref) in zip(dic_results_candidate.items(), dic_results_reference.items()):
			number_candidate = num_cand
			lst_candidate = result_cand
			lst_reference = result_ref

		for index_candidate, element_candidate in enumerate(lst_candidate):
			for index_reference, element_reference in enumerate(lst_reference):
				if element_candidate == element_reference:
					div += 1 / (log(fabs(index_candidate - index_reference) + 2))
			D_max += 1 / (log(2))
		score = div / D_max
		return number_candidate, score

