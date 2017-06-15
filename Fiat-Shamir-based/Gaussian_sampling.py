from math import exp
import random
# to do statiscal tests
def Bernoulli_rv(c):
	'''
		c is a parameter of Bernoulli distribution
	'''
	return 1 if random.random() < c else 0

def Bernoulli_exp(x, f):
	'''
	Description:
	Algorithm 8 in BLISS paper

	Sample according to exp(-x/f) for x E [0,2^l)
	or x is an integer in binary form of lenght l
	f is a real.

	i/p:
	x: int
	f: float
	'''
	bin_rep = map(int, list(bin(x)[2:])) # list with 0's and 1's reprsenting x. msb is first as usual
	l = len(bin_rep) 
	# Precomputation requires only log(x) base 2 number of elements  
	c = [exp(-float(2**i) / f) for i in range(0, l)] # Ci stores exp(-2^i / f)

	# starting from l-1, as then smallest probabilities are checked first and algorithm terminates faster 
	for i in range(0, l):
		if(bin_rep[i]):
			A = Bernoulli_rv(c[l-i-1])
			if not A:
				return 0
	return 1

def Bernoulli_cosh(x, f):
	'''
	Sample according to 1/cosh(x/f)
	Extends corollary 6.4 from BLISS paper
	'''
	powx = abs(x)
	while(True):
		A = Bernoulli_exp(powx, f) # each iteration this changes as randomness comes from Bernoulli_exp exp(-|x|/f)
		if(A):
			return 1
		B = Bernoulli_rv(0.5)
		if not(B or A):			# todo: check whether it is OR with the same Bexp or diff
			return 0

def disc_Gaussian_sampling():
	pass
	
'''
def Bernoulli_frac_op(a, b):
	
	#Description:
	#Algorithm 9 in BLISS paper
	#This is just for validating lemma 6.3 in the paper
	#Use it as a template

	#Sampling Ba op Bb  which is the same as Ba/(1-(1-a)*b)  

	#i/p: a and b which are the parameters for the Bernoulli distribution Ba and Bb
	
	while(True):
		A = Bernoulli_rv(a)
		if(A == 1):
			return 1
		B = Bernoulli_rv(b)
		if(B == 0):
			return 0
'''				


	