#!/usr/bin/python
""" Simple implementation using the old RANDOM.ORG API
	to be used in Randomized Algorithms (Fall 2014) @
	Aarhus Univeristy, Denmark
	Author: Martin Storgaard
	E-mail: 201400002@post.au.dk
"""
import sys		# sys.exit
import urllib	# urllib.urlencode
import urllib2	# Handle the random.org api
import shelve	# Database handling
from math import ceil

def getQuota():
	"""	The Quota Checker allows you to examine your quota 
		at any point in time. If the quota is exceeded or
		any error occurs during this process, the program
		would exit.
	"""
	try:
		req = urllib2.Request('http://www.random.org/quota/?format=plain')
		response = urllib2.urlopen(req)
		return int(response.read())
	except urllib2.HTTPError as e:
		print 'Could not get quota, HTTP error code', e.code,
		if e.code == 503:
			print 'i.e. your quota is exceeded.'
		sys.exit(1)
	except urllib2.URLError as e:
		print 'Could not get quota:', e.reason[1]
		sys.exit(1)

def getIntegers(minimum, maximum, num, base = 10, rnd = 'new'):
	"""	The Integer Generator will generate truly random 
		integers in configurable intervals. If the quota 
		is exceeded or any error occurs during this 
		process, the program would exit.
		
		Parameters
		----------
		minimum : int
			The minimum number to be generated. Must
			be smaller than maximum and 1e9 and 
			larger than -1e9
		maximum : int
			The minimum number to be generated. Must
			be larger than minimium and -1e9 and less
			than 1e9
		num : int
			The number of truely random integers wanted.
			Must be larger than 1 and less than 1e4
		base : int
			The base random numbers should be represented
			as (although they would be casted to an int).
			Must be either 2, 8, 10 or 16
		rnd : string
			Determines the randomization to use to generate
			the numbers. Either 'new', id.identifier
			(the identifier is used to determine the
			randomization in a deterministic fashion from a 
			large pool of pregenerated random bits) or a
			date in ISO 8601 format (i.e., YYYY-MM-DD) or one
			of the two shorthand strings today or yesterday.
	"""
	if num < 1 or num > 1e4:
		return
	elif minimum < -1e9 or minimum > 1e9:
		return
	elif maximum < -1e9 or maximum > 1e9:
		return
	elif minimum > maximum:
		return
	elif base not in [2, 8, 10, 16]:
		return
	# Encode the parameters
	data = urllib.urlencode({
		'num': num,
		'min': minimum,
		'max': maximum,
		'col': 1,
		'base': base,
		'format': 'plain',
		'rnd': rnd
	})
	
	# Ask for random numbers
	try:
		req = urllib2.Request('http://www.random.org/integers/?' + data)
		response = urllib2.urlopen(req)
	except urllib2.HTTPError as e:
		print 'Could not get integers, HTTP error code', e.code, e.read()
		sys.exit(1)
	except urllib2.URLError as e:
		print 'Could not get integers:', e.reason[1]
		sys.exit(1)
		
	# Result
	result = []
	# A small speed-up by making the method local
	app = result.append
	# If we succed to get all integers, read them!
	for integer in response.readlines():
		app(int(integer.strip()))
	return result

if __name__ == '__main__':
	from threading import Thread
	
	def saveIntegers(db, integers):
		l = db['len']
		db[str(l)] = [int(i) for i in integers]
		db['len'] = l + 1
		
		
	# Print how to close to aviod corruption
	# in the database!
	print '========================='
	print 'Notice: Close with Ctrl-C'
	print '========================='
	minimum = int(-1e9)
	maximum = int(1e9)
	bytesUsed = max(minimum.bit_length(), maximum.bit_length())/8.0
	db = shelve.open('randomNumbers.db', 'c')
	# Create and initilize the database if needed
	if 'len' not in db:
		db['len'] = 0
		
	# Get first batch
	q = getQuota()
	if q < 1:
		sys.exit(0)
	num = min(1e4, ceil(q/bytesUsed))
	rn = getIntegers(minimum, maximum, num)
	while True:# Save the integers in such a way, that they will
		# complete even on a keyboard interrupt
		a = Thread(target=saveIntegers, args=(db, rn))
		a.start()
		# Ask for the next batch while saving the old ones
		q = getQuota()
		if q < 1:
			break
		num = min(1e4, ceil(q/bytesUsed))
		rn = getIntegers(minimum, maximum, num)
		# Do not continue until the old is saved
		a.join()
