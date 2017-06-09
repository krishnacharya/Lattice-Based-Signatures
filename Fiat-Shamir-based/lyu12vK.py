'''
Authors: Krishna Acharya, Sannidhya Shukla, Dheeraj Pai 
Date:	7 June 2017
Brief Description:
Lattice Based Signature Based on the Fiat Shamir Framework
employs Unimodal Gaussian for Rejection sampling
based on Vadim Lyubachevsky's Eurocrypt 2012 paper.
Parameters of the signature scheme are based on SIS q,n,m,d
'''
#!/usr/bin/env sage
import sys
from sage.all import * 
from sage.stats.distributions.discrete_gaussian_lattice import DiscreteGaussianDistributionLatticeSampler
import numpy as np
import util
import random
from math import exp
from random import SystemRandom

#SIS parameters
n,m,k,d,q = 128,1000,20,1,114356107 # these parameters must be carefully adjusted
b = 2*d + 1  # range for the Signing Key matrix
M = 2.72   # the real value such that f(x) <= M * g(x), and an element from g(x) is accepted with probability f(x)/M*g(x)

#Discrete Gaussian
st_dev = 300
D = DiscreteGaussianDistributionLatticeSampler(ZZ**m, st_dev) # discrete gaussian used to sample y which hides Sc, to prevent signing key leak
eta = 1.1

def KeyGen():
	'''
		input:
		q : polynomial size prime number
		n, m, k : matrix dimensions specifiers
		d : SIS parameter, hardest instances are where d ~ q^(n/m)
		d < q
		output:
		Signing Key S :  Matrix of dimension mxk with coefficients in 
		Verification Key A : Matrix of dimension nxm with coefficients from 
		T : the matrix AS ,it is used in the Verification of the signature

	'''
	#global n,m,k,d,q,b
	S = util.crypt_secure_matrix(b, m, k)
	A = util.crypt_secure_matrix(q, n, m)
	T = np.matmul(A, S) % q	
	return S, A, T

def Sign(msg, A, S):
	'''
		i/p:
		msg: string, which the sender wants to brodcast
		A  : numpy array, Verification Key dimension nxm
		S  : numpy array, Signing key dimension mxk

		o/p:
		(z,c) : signature		
	'''
	#global n,m,k,d,q,st_dev,M		
	count = 0
	while(True):
		y = np.array(D()) # discrete point in Zq^m
		c = util.hash_to_baseb(np.matmul(A,y) % q, msg, 3, k)  # 3 because we want b/w 0,1,2 small coefficients in Zq
		Sc = np.matmul(S,c)
		z = Sc + y		
		try:					
			pxe = float(-2*z.dot(Sc) + Sc.dot(Sc))
			val = exp(pxe / (2*st_dev**2)) / M							
		except OverflowError:
			print "OF"			
			continue			
		if(random.random() < min(val, 1.0)):
			break
		if(count > 20): # beyond 20 rejection sampling loops then end 
			return 0.0,0.0
		count += 1								
	return z,c

def Verify(msg, z, c, A, T):
	'''
		Verification for the signature
		i/p:
		msg: the string sent by the sender
		(z,c): vectors in Zq, the signature
		A  : numpy array, Verification Key dimension nxm
		T : the matrix AS mod q ,it is used in the Verification of the signature
	'''	
	comp = eta * st_dev * np.sqrt(m)
	# checks for norm of z being small and that H(Az-Tc mod q,msg) hashes to c			
	if np.sqrt(z.dot(z)) <= comp and np.array_equal(c,util.hash_to_baseb(np.array(np.matmul(A,z) - np.matmul(T,c)) % q, msg, 3, k)):
		return True
	else:
		return False

def test():	
	S, A, T =  KeyGen()
	z, c = Sign("hellohow",A, S)
	print Verify("hellohow",z,c,A,T)
	print Verify("helooooo",z,c,A,T)
	print Verify("jkaflkaf",z,c,A,T)
test()	