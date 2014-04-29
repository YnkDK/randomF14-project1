#!/usr/bin/python
"""	Implementation code for Project 1 in Randomized Algorithms
	(Fall 2014). Implementation of the FIND algorithm with
	appropriate counters.
	Authors: 	Martin Storgaard, Jon Bjerrum Jacobsen, 
				Anders Strand-Holm Vinther
	E-mails: 	{201400002, 20117331, 20033980}@post.au.dk
"""
import sys	# sys.exit
import shelve # Database with random numbers
import anydbm

def next():
	"""	Returns the next random number found in the database.
		If no such number was found, the program exists.
	"""
	if len(next.current) == 0:
		# Get the next block of random numbers
		next.i += 1
		if next.i == next.db['len']:
			print next.i, 'is larger than the database size!'
			sys.exit(1)
		next.current = next.db[str(next.i)]
	return next.current.pop(0)

# Initilize 'static' variables for next
try:
	next.db = shelve.open('randomNumbers.db', 'r')
	next.current = next.db['0']
	next.i = 1
except anydbm.error as e:
    del globals()[next.func_name]



def generateL(n, rng = None):
	"""	Generates a nonempty list of distinct numbers
	
		Parameters
		----------
		n : int
			The length of the list
	"""
	if rng is None:
		if n < 1:
			return [next()]
		# Ensure unique integers
		L = set()
		add = L.add
		while len(L) < n:
			add(next())
		return list(L)
	else:
		if n < 1:
			return [rng.randint(int(-1e9), int(1e9))]
		L = set()
		add = L.add
		while len(L) < n:
			add(rng.randint(int(-1e9), int(1e9)))
		return list(L)

def find(L, k, rng = None):
	"""	Finds the k'th element in L
	"""
	find.cmp = 0
	# Find k'th element on a copy of L
	if rng is None:
		return findRec(list(L), k, 1)
	else:
		return findRecMT(list(L), k, 1, rng)

def findRecMT(L, k, d, rng):
	# Line 1
	# Select e randomly from L using the uniform distribution
	e = rng.choice(L)
	
	# Line 2
	# Split L' = L - {e} into the two sublists
	# 	L1 = [ai in L | ai < e]
	#	L2 = [ai in L | ai > e]
	# by comparing e to each element in L'
	L.remove(e)
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
	if lenL1 > k:
		# If |L1| > k then make a recursive call on L1 and k
		return findRecMT(L1, k, d + 1, rng)
	elif lenL1 < k:
		# If |L1| < k then make a recursive call on L1 and k - 1 - |L1|
		return findRecMT(L2, k - 1 - lenL1, d + 1, rng)
	else:
		# Return e
		return e, d, find.cmp
		
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
	if lenL1 > k:
		# If |L1| > k then make a recursive call on L1 and k
		return findRec(L1, k, d + 1)
	elif lenL1 < k:
		# If |L1| < k then make a recursive call on L1 and k - 1 - |L1|
		return findRec(L2, k - 1 - lenL1, d + 1)
	else:
		# Return e
		return e, d, find.cmp
		
def runExperiments(n, rng = None):
	"""	Runs 1.2*n experiments on k = 0, n/4, n/2, 3n/4, n-1
		and writes the output to stdout. Furthermore a naive
		control of correctness is performed.
		
		Parameters
		----------
		n : int
			The length of the lists used in the experiments
	"""
	res1 = []
	res2 = []
	runs = int(1.2*n)
	# Make at least n runs
	for i in range(runs):
		# Generate the list
		L = generateL(n, rng)
		# Sort it for later use
		sortedL = sorted(L)
		for k in [0, n/4, n/2, 3*n/4, n-1]:
			# Find k in L
			res = find(L, k, rng)
			# Naive correctness test :)
			if int(sortedL[k]) is not int(res[0]):
				# If the algorithm is wrong, STOP!
				print "Looked for", sortedL[k], "but got", res[0]
				sys.exit(1)
			# Print the result (pipe to a file)
			#print int((1000.0*i)/runs)/10.0, i, n, kStr[kIndex], res[1], res[2]
			res1.append(res[1])
			res2.append(res[2])
	return res1, res2
		
if __name__ == '__main__':
	import random
	from numpy import median
	
	if len(sys.argv) == 2 and sys.argv[1] == 'randomNumbers.db':
		selections, comparisons = runExperiments(int(1e2))
		print int(1e2), max(selections), min(selections), float(sum(selections))/len(selections), median(selections)
		print int(1e2), max(comparisons), min(comparisons), float(sum(comparisons))/len(comparisons), median(comparisons)
		selections, comparisons = runExperiments(int(1e3))
		print int(1e3), max(selections), min(selections), float(sum(selections))/len(selections), median(selections)
		print int(1e3), max(comparisons), min(comparisons), float(sum(comparisons))/len(comparisons), median(comparisons)
		selections, comparisons = runExperiments(int(1e4))
		print int(1e4), max(selections), min(selections), float(sum(selections))/len(selections), median(selections)
		print int(1e4), max(comparisons), min(comparisons), float(sum(comparisons))/len(comparisons), median(comparisons)
	else:
		# Seed from
		# http://www.random.org/strings/?num=1&len=20&digits=on&upperalpha=on&loweralpha=on&unique=off&format=plain&rnd=date.2014-04-01
		random.seed('bmMNXgGHmg0DQ9rYmoYy')
		selections, comparisons = runExperiments(int(1e2), random)
		print int(1e2), max(selections), min(selections), float(sum(selections))/len(selections), median(selections)
		print int(1e2), max(comparisons), min(comparisons), float(sum(comparisons))/len(comparisons), median(comparisons)
		selections, comparisons = runExperiments(int(1e3), random)
		print int(1e3), max(selections), min(selections), float(sum(selections))/len(selections), median(selections)
		print int(1e3), max(comparisons), min(comparisons), float(sum(comparisons))/len(comparisons), median(comparisons)
		selections, comparisons = runExperiments(int(1e4), random)
		print int(1e4), max(selections), min(selections), float(sum(selections))/len(selections), median(selections)
		print int(1e4), max(comparisons), min(comparisons), float(sum(comparisons))/len(comparisons), median(comparisons)	
	
	print next.i
