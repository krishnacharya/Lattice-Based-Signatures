'''
Transcedental function Bernoulli sampling, Gaussian sampling
used for embedded devices where floating point computations
are not native and memory is limited.
'''
from math import exp
import random

def Bernoulli_rv(c):
	'''
		c is a parameter of Bernoulli distribution
	'''
	return 1 if random.random() < c else 0


# Precomputation for Bernoulli_exp(x)
f = 3 # fixed real 
l = 64 # max number of bits in positive integer x
c = [exp(-float(2**i) / f) for i in range(0, l)] # Ci stores exp(-2^i / f)

def Bernoulli_exp(x):
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
	d = len(bin_rep) # length of the current integer in binary, d < l

	# starting from l-1, as then smallest probabilities are checked first and algorithm terminates faster 
	for i in range(0, d):
		if(bin_rep[i]):
			A = Bernoulli_rv(c[d-i-1])
			if not A:
				return 0
	return 1

# uses the same fixed real f
def Bernoulli_cosh(x):
	'''
	Sample according to 1/cosh(x/f)
	Extends corollary 6.4 from BLISS paper
	'''
	powx = abs(x)
	while(True):
		A = Bernoulli_exp(powx) # each iteration this changes as randomness comes from Bernoulli_exp exp(-|x|/f)
		if(A):
			return 1
		B = Bernoulli_rv(0.5) or Bernoulli_exp(powx)  # has to be seperate Bernoulli_exp(powx) call as we dont want dependence on A
		if not(B):			
			return 0

def disc_Gaussian_sampling():
	pass
	