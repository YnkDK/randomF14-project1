#!/usr/bin/python -u
"""	Implementation code for Project 1 in Randomized Algorithms
	(Fall 2014). Implementation of the Randomized Quicksort 
	algorithm with appropriate counters.
	Authors:	Martin Storgaard, Jon Bjerrum Jacobsen, 
				Anders Strand-Holm Vinther
	E-mails: 	{201400002, 20117331, 20033980}@post.au.dk
"""

import sys # sys.exit(1) if randQS does not work correctly

def generateL(n):
	"""	Generates a nonempty list of distinct numbers between
		-10**9 and 10**9. The interval is determined by the
		limitations of RANDOM.ORG
	
		Parameters
		----------
		n : int
			The length of the list
	"""
	if n < 1:
		return [random.randint(int(-1e9), int(1e9))]
	L = set()
	add = L.add
	while len(L) < n:
		add(random.randint(int(-1e9), int(1e9)))
	return list(L)
	
def randQS(S, c = 0):
	""" Sorts the set S using the randomized Quicksort
		described in [MR95] page 4 (RandQS). Returns a
		tuple (sorted list, number of comparisons).
		
		Parameters
		----------
		S : list
			A list of (distinct) numbers (or any type
			that can be compared using "<" operator.
		c : int
			The number of comparisons made thus far.
	"""
	# Stop sorting if the list is empty
	if not S:
		return [], 0
	# Choose an element y uniformly at random from S:
	# every element in S has equal probability of being chosen
	y = random.choice(S)
	# We do not want y in any sublist
	S.remove(y)
		
	# By comparing each element of S with y, determine the set
	# S1 if ekenebts snakker than y and the set S2 of elements
	# larger than y
	S1, S2 = [], []
	# Making append local is a little speed-up
	app1, app2 = S1.append, S2.append
	for element in S:
		(app1 if element < y else app2)(element)

	# Recursivly sort S1 and S2 keeping track of the number of
	# comparisons made
	s1, c1 = randQS(S1, c)
	s2, c2 = randQS(S2, c)
	# Output the sorted version of S1, followed by y, and then
	# the sorted version of S2, along with the total number of
	# comparisons made
	return s1 + [y] + s2, len(S) + c1 + c2

    
def runExperiments(n):
	"""	Runs 1.2*n experiments. It uses the built-in function
		"sorted" as a test of correction, which runs in O(n)
		if it is correct (timsort). It returns the average
		number of comparisons made by randQS.
		
		Parameters
		----------
		n : int
			The length of the lists used in the experiments
	"""
	runs = int(2*1.2*n)
	
	cmps = 0.0
	# Make at least n runs
	for i in range(runs):
		# Generate the list
		L = generateL(n)
		# Sort it
		result, c = randQS(L)
		# Use timsort to check if it was successfully sorted
		if result != sorted(result):
			sys.exit(1)
		# Aggregate the comparisons made so far
		cmps += c
	# Return the average number of comparisons
	return cmps/runs
		
		
if __name__ == '__main__':
	import random

	# Seed from
	# http://www.random.org/strings/?num=3&len=20&digits=on&upperalpha=on&loweralpha=on&unique=off&format=plain&rnd=date.2014-04-02
	random.seed('cVlcikgZ7P5QNY7DL2C8HXDx5d0jTy3DypwgmaqYIa5B0wMP4pvPZlepIH4H')

	print "($n=10^2$, %f)" % runExperiments(int(1e2)),
	print "($n=10^3$, %f)" % runExperiments(int(1e3)),
	print "($n=10^4$, %f)" % runExperiments(int(1e4))
