#!/usr/bin/python
""" Implementation code for Project 1 in Randomized Algorithms
	(Fall 2014). Implementation of the FIND algorithm with
	appropriate counters.
	Authors: 	Martin Storgaard, Jon Bjerrum Jacobsen, 
				Anders Strand-Holm Vinther
	E-mails: 	{201400002, 20117331, 20033980}@post.au.dk
"""

def next():
	""" Returns the next random number. Prints a warning if
		the random numbers starts a new period.
	"""
	next.current += 1
	if next.current == next.len:
		next.current = 0
		print "================================================"
		print "WARNING: The random numbers starts a new period!"
		print "================================================"
	return int(next.integers[next.current])
	
# Init static variables if the method next
with open('randomNumbers.txt', 'r') as r:
	next.integers = r.read().strip().split(' ')
	next.current = -1
	next.len = len(next.integers)

def generateL(n):
	""" Generates a nonempty list of distinct numbers
	"""
	if n < 1:
		return [next()]
	L = set()
	while len(L) < n:
		L.add(next())
	return list(L)

if __name__ == '__main__':
	print generateL(10)
