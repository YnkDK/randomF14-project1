#!/usr/bin/python
""" Implementation code for Project 1 in Randomized Algorithms
	(Fall 2014). Implementation of the FIND algorithm with
	appropriate counters.
	Authors: 	Martin Storgaard, Jon Bjerrum Jacobsen, 
				Anders Strand-Holm Vinther
	E-mails: 	{201400002, 20117331, 20033980}@post.au.dk
"""
import sys	# sys.exit
import shelve # Database with random numbers
from math import ceil
from os import stat

def next():
	next.i += 1
	if next.i > next.db['len']:
		print next.i, 'is larger than the database size!'
		sys.exit(1)
	return next.db[str(next.i)]
	
next.i = 0
next.db = shelve.open('randomNumbers.db', 'r')


def generateL(n):
	""" Generates a nonempty list of distinct numbers
	
		Parameters
		----------
		n : int
			The length of the list
	"""
	if n < 1:
		return [next()]
	# Ensure unique integers
	L = set()
	while len(L) < n:
		L.add(next())
	return list(L)

def find(L, k):
	find.cmp = 0
	return findRec(list(L), k, 1)

def findRec(L, k, d):
	# Line 1
	# Select e randomly from L using the uniform distribution
	tmp = next()
	ie = tmp % len(L)
	e = L[ie]
	
	# Line 2
	# Split L' = L - {e} into the two sublists
	# 	L1 = [ai in L | ai < e]
	#	L2 = [ai in L | ai > e]
	# by comparing e to each element in L'
	del L[ie]
	L1 = []
	L2 = []
	app1 = L1.append
	app2 = L2.append

	find.cmp += len(L)
	for element in L:
		if element < e:
			app1(element)
		else:
			app2(element)
	
	# Line 3
	lenL1 = len(L1)
	# If |L1| > k - 1 then make a recursive call on L1 and k
	if lenL1 > k:
		return findRec(L1, k, d + 1)
	elif lenL1 < k:
		return findRec(L2, k - 1 - lenL1, d + 1)
	else:
		return e, d, find.cmp
		
def runExperiments(n):
	kStr = ['"0"', '"n/4"', '"n/2"', '"3n/4"', '"n-1"']
	runs = int(1.5*n)
	# Make at least n runs
	for i in range(runs):
		# Generate the list
		L = generateL(n)
		# Sort it for later use
		sortedL = sorted(L)
		# Index in the kStr that are currently used
		kIndex = 0
		for k in [0, n/4, n/2, 3*n/4, n-1]:
			# Find k in L
			res = find(L, k)
			# Naive correctness test :)
			if int(sortedL[k]) is not int(res[0]):
				# If the algorithm is wrong, STOP!
				print "Looked for", sortedL[k], "but got", res[0]
				sys.exit(1)
			# Print the result (pipe to a file)
			print int((1000.0*i)/runs)/10.0, i, n, kStr[kIndex], res[1], res[2]
			# Go to next k
			kIndex += 1
		
if __name__ == '__main__':
	runExperiments(int(1e2))
	runExperiments(int(1e3))
	runExperiments(int(1e4))
	
	print next.i
