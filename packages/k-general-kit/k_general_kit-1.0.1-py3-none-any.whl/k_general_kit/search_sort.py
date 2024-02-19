#!/usr/bin/env python3
# -*-coding:UTF-8 -*

import math
from k_general_kit.gen_obj import real

"""Search Functions"""

def seq_search(x, I, start:int=0, end:int=-1)-> int:
	"""It returns the first found index in [start, end[ of x in an indexable iterable I, and -1 else. It uses the sequential search principle.
	The average complexity is O(end-start)."""
	l = len(I)
	if end == -1:
		end = l
	else:
		end = min(end, l)
	for i in range(start, end):
		if I[i] == x:
			return i
	return -1

def dich_search(x, I, start:int=0, end:int=-1)-> int:
	"""It returns the first found index in [start, end[ of x in an indexable iterable I (ordered between the indices start and end-1), and -1 else. It uses the dichotomic search principle.
	The average complexity is O(log(end-start))."""
	l = len(I)
	assert start >= 0
	if end == -1:
		end = l
	else:
		end = min(end, l)
	if  start >= end:
		return -1
	mid = int((end+start)/2)
	y = I[mid]
	if y == x:
		return mid
	if (x-y)*(y-I[start]) >= 0: #In this case, independently of the way I[start, end[ is ordered; if x is in I, thus, the index of x is > mid
		return dich_search(x, I, mid+1, end)
	return dich_search(x, I, start, mid)

def interpol_search(x, I, start:int=0, end:int=-1)-> int:
	"""It returns the first found index in [start, end[ of x in an ordered indexable iterable I (ordered between the indices start and end-1), and -1 else. It uses the interpolation search principle.
	The average complexity is O(log(log(end-start))). The more the curve y = I[i] is linear, the better is the algorithm."""
	l = len(I)
	assert start >= 0
	if end == -1:
		end = l
	else:
		end = min(end, l)
	if  start >= end:
		return -1
	if I[end-1] == I[start]: #Due to the fact that I is ordered, we necessarily have I[i] = I[0] for all possible i.
		if I[start] == x:
			return start
		return -1
	pos = int((x-I[start])*(end-1-start)/(I[end-1]-I[start])+start)
	if pos < start or pos >= end:
		return -1
	y = I[pos]
	if y == x:
		return pos
	if (x-y)*(y-I[start]) >= 0: #In this case, independently of the way I is ordered, if x is in I, thus, the index of x is > pos
		return interpol_search(x, I, pos+1, end)
	return interpol_search(x, I, start, pos)

def exp_search(x, I, start:int=0, end:int=-1)-> int:
	"""It returns the first found index in [start, end[ of x in an ordered indexable iterable I (ordered between the indices start and end-1), and -1 else. It uses the exponential search principle.
	It is useful when we manipulate very large iterable in term of length. It reduces first the domain of search, before applying the interpol search"""
	l = len(I)
	assert start >= 0
	if end == -1:
		end = l
	else:
		end = min(end, l)
	if  start >= end:
		return -1
	#We look for the samllest i such that 2**i>=start
	if start == 0:
		i = 0
	else:
		i = math.ceil(math.log2(start))
	pos = min(2**i, end-1)
	y = I[pos]
	if y == x:
		return pos
	if (y-I[start])*(x-y) < 0: #In this case, independently of the way I is ordered, if x is in I, thus, the index of x is in [start and pos[
		return interpol_search(x, I, start, pos)
	i += 1
	#We look for the smallest i such that x is between I[2**(i-1)] and I[2**i], with i >= 2
	isup = math.log2(end)
	while i < isup:
		pos = 2**i
		y = I[pos]
		if y == x:
			return pos
		if (y-I[start])*(x-y) < 0: #In this case, independently of the way I is ordered, if x is in I, thus, the index of x is in ]2**(i-1) and pos[
			return interpol_search(x, I, 2**(i-1)+1, pos)
		i += 1
	print(2**(i-1)+1, end)
	return interpol_search(x, I, 2**(i-1)+1, end)

"""Sort Functions"""

def bubble_sort(L: list[real|str], start: int = 0, end: int = -1, ord: int = 0):
	"""
	This function sorts a list L[start:end] in ascending order if ord=0 and in descending order if ord=1 using the Bubble sort principle.

	Parameters:
	L (list): The list to be sorted.
	start (int): Starting index of the list to be sorted. Default is 0.
	end (int): Ending index of the list to be sorted. Default is -1, which means sorting up to the end of the list.
	ord (int): The sorting order. 0 for ascending order and 1 for descending order. Default is 0.

	Example:
	>>> L = [3, 5, 1, 4]
	>>> bubble_sort(L)
	>>> print(L)
	[1, 3, 4, 5]

	"""

	# Get the length of the list
	l = len(L)

	# If end index is greater than the length of the list, set it to the length of the list
	if end == -1 or end > l:
		end = l

	# Traverse through the list from end-1 to start+1 with a step of -1
	for i in range(end-1, start+1, -1):

		# Traverse through the list from start to i
		for j in range(start, i):

			# Compare adjacent elements and swap them if necessary based on the sorting order
			if (L[j] > L[j+1])+ord == 1:
				L[j], L[j+1] = L[j+1], L[j]

def select_sort(L:list[real|str], start:int = 0, end:int = -1, ord:int = 0):
	"""It returns the sorted version of a list L[start: end[ in the ascending order if ord = 0 amd in the descending order if ord = 1
	NB: It uses the selection sort principle"""
	assert start >= 0
	l = len(L)
	if end == -1:
		end = l
	for i in range(start, end-1):
		m = i
		for j in range(i+1, end):
			if (L[j]<L[i])+ord == 1:
				m = j
		L[i], L[m] = L[m], L[i]

def insert_sort(L:list[real|str], start:int = 0, end:int = -1, ord:int = 0)-> list:
	"""It returns the sorted version of a list L[start: end[ in the ascending order if ord = 0 amd in the descending order if ord = 1
	NB: It uses the insertion sort principle"""
	assert start >= 0
	l = len(L)
	if end == -1:
		end = l
	for i in range(start+1, end):
		x = L[i]
		j = i-1
		while j >= start and (L[j]>x)+ord == 1:
			L[j+1] = L[j]
			j -= 1
		L[j+1] = x

def count_sort(L:list[real], start:int = 0, end:int = -1, step:float = 1, m:float = -math.inf, M:float = math.inf, ord:int = 0):
	"""It returns the sorted version of a list L [start: end[ in the ascending order if ord = 0 amd in the descending order if ord = 1
	NB: It uses the counting sort principle; Thus, it takes as parameter a step, which indicates the samllest distance between 2 elts of L, and so that each distance between 2 elts of L is a multiple of step.
	m and M, if given (what is advised to ameliorate the sort time) are the minimum and maximum of elts of L[start: end]."""
	assert start >= 0 and step > 0
	l = len(L)
	if end == -1:
		end = l
	#We look for the bounds of I
	if start >= end-1:
		return
	if m == -math.inf:
		m = min(L[start: end])
	if M == math.inf:
		M = max(L[start: end])
	if ord == 0:
		Occ = {m+i*step:0 for i in range(int((M-m)/step)+1)}
	else:
		Occ = {M-i*step:0 for i in range(int((M-m)/step)+1)}
	for x in L[start: end]:
		Occ[x] += 1
	i = start
	for x, n in Occ.items():
		L[i: i+n] = [x]*n
		i += n

def part_list(L:list[real|str], start:int = 0, end:int = -1, ord:int = 0, pivot:int = -1)-> int: 
	"""It arranges a list L = L[start: end[ such that al elts < L[pivot] are before L[pivot] and all elts >= L[pivots] are after it, if ord = 0. It does the contrary else.
	It returns the final position of L[pivot]
	Rk: It optimises the space complexity by staying in the same list; however, time complexity worsens with the permutations."""
	assert start >= 0
	l = len(L)
	if end == -1:
		end = l
	assert end > start
	if pivot != -1:
		assert start <= pivot <= end-1
		L[pivot], L[end-1] = L[end-1], L[pivot]
	Pivot = L[end-1]
	pos = start #We initialise the position of the pivot = L[pivot] and we'll update it in the next part
	for i in range(start, end-1):
		if (L[i] < Pivot)+ord == 1:
			L[pos], L[i] = L[i], L[pos]
			pos += 1
	L[pos], L[end-1] = L[end-1], L[pos]
	return pos

def part_list2(L:list[real|str], start:int = 0, end:int = -1, ord:int = 0, pivot:int = -1)-> int: 
	"""It arranges a list L = L[start: end[ such that al elts < L[pivot] are before L[pivot] and all elts >= L[pivots] are after it, if ord = 0. It does the contrary else.
	It returns the final position of L[pivot]s
	Rk: It optimises time complexity by sacrificing space complexity."""
	assert start >= 0
	l = len(L)
	if end == -1:
		end = l
	assert end > start
	if pivot == -1:
		pivot = end-1
	else:
		assert start <= pivot <= end-1
	Before, After = [], []
	Pivot = L[pivot]
	pos = start
	for elt in L[start: pivot]+L[pivot+1: end]:
		if (elt < Pivot)+ord == 1:
			Before.append(elt)
			pos += 1
		else:
			After.append(elt)
	L[start: end] = Before+[Pivot]+After
	return pos

def quick_sort(L:list[real|str], start:int = 0, end:int = -1, ord:int = 0, pivot:int = -1):
	"""It returns the sorted version of a list L[start: end[ in the ascending order if ord = 0 amd in the descending order if ord = 1
	NB: It uses the quick sort principle.
	Rk: This version uses part_list(), and so optimises most space complexity."""
	assert start >= 0
	l = len(L)
	if end == -1:
		end = l
	if end <= start+1:
		return
	if pivot == -1:
		pivot = end-1
	else:
		assert start <= pivot <= end-1
	pos = part_list(L, start, end, ord, pivot)
	quick_sort(L, start, pos, ord, -1)
	quick_sort(L, pos+1, end, ord, -1)

def quick_sort2(L:list[real|str], start:int = 0, end:int = -1, ord:int = 0, pivot:int = -1):
	"""It returns the sorted version of a list L[start: end[ in the ascending order if ord = 0 amd in the descending order if ord = 1
	NB: It uses the quick sort principle.
	Rk: This version uses part_list2(), and so optimises most time complexity."""
	assert start >= 0
	l = len(L)
	if end == -1:
		end = l
	if end <= start+1:
		return
	if pivot == -1:
		pivot = end-1
	else:
		assert start <= pivot <= end-1
	pos = part_list2(L, start, end, ord, pivot)
	quick_sort(L, start, pos, ord, -1)
	quick_sort(L, pos+1, end, ord, -1)

def quick_sort3(L: list[real|str], start: int = 0, end: int = -1, ord: int = 0, pivot: int = -1):
	"""
	This function sorts a list L[start: end[ in ascending or descending order using the Quick _sort Algorithm.
	
	Args:
		L (list[real|str]): The list to be sorted
		start (int): The starting index of the sublist to be sorted (default is 0)
		end (int): The ending index of the sublist to be sorted (default is -1)
		ord (int): The order of sorting: 0 for ascending and 1 for descending (default is 0)
		pivot (int): The index of the pivot element (default is -1)
	
	Returns:
		list[real|str]: The sorted list
	"""
	# If the end index is not specified, set it to the last index of the list
	if end == -1:
		end = len(L)
	
	# If there are no elements between the start and the end indices, return the list as is
	if end <= start+1:
		return
	
	end -= 1
	# If the pivot index is not specified, set it to the last index of the sublist
	if pivot == -1:
		Pivot = L[end]
	else:
		Pivot = L[pivot]
		L[end], L[pivot] = Pivot, L[end]
	
	# Set the indices i1 and i2 to the start and end-1 indices respectively
	i1, i2 = start, end-1
	
	# Loop until i1 is greater than i2
	while i1 <= i2:
		# Move i2 to the left until an element less than the pivot is found (case ord=0)
		while i2 >= i1 and (L[i2] >= Pivot) + ord == 1:
			L[i2+1] = L[i2]
			i2 -= 1
		
		# Move i1 to the right until an element greater than the pivot is found (case ord=0)
		while i1 <= i2 and (L[i1] <= Pivot) + ord == 1:
			i1 += 1
		
		# Swap the elements at indices i1 and i2 because there are not supposed to be at their current positions
		if i1 <= i2 and (L[i2] < Pivot) + ord == 1 and (L[i1] > Pivot) + ord == 1:
			L[i1], L[i2] = L[i2], L[i1]
			i1 += 1
	
	# Place the pivot element in its final correct position
	L[i1] = Pivot
	
	# Recursively sort the sublists on either side of the pivot
	quick_sort3(L, start, i1, ord, -1)
	quick_sort3(L, i1+1, end+1, ord, -1)

def merge_list(L1:list[real|str], L2:list, ord:int = 0)-> list[real|str]:
	"""It merges conserving the order, 2 ordered lists in the ascending order (if ord = 0) or in the descending order (if ord = 1)."""
	if L1 == []:
		return L2
	if L2 == []:
		return L1
	if (L1[0] < L2[0])+ord == 1:
		return [L1[0]]+merge_list(L1[1:], L2, ord)
	return [L2[0]]+merge_list(L1, L2[1:], ord)

def merge_sort(L:list[real|str], start:int = 0, end:int = -1, ord:int = 0):
	"""It returns the sorted version of a list L[start: end] in the ascending order if ord = 0 amd in the descending order if ord = 1
	NB: It uses the merge sort principle."""
	assert start >= 0
	l = len(L)
	if end == -1:
		end = l
	if end <= start+1:
		return L
	mid = int((start+end)/2)
	L1, L2 = L[start: mid], L[mid: end]
	merge_sort(L1, ord = ord)
	merge_sort(L2, ord = ord)
	L[start: end] = merge_list(L1, L2, ord = ord)

if __name__ == '__main__':
	import search_sort
	help(search_sort)
	input("Glad to have served you! Press 'Enter' to quit.")