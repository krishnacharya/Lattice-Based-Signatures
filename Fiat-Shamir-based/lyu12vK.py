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

def KeyGen(**kwargs):
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
	q, n, m, k, d = kwargs['q'], kwargs['n'], kwargs['m'], kwargs['k'], kwargs['d']
	S = util.crypt_secure_matrix(-d, d, m, k)
	A = util.crypt_secure_matrix(-(q-1)/2, (q-1)/2, n, m)
	T = util.matrix_to_Zq(np.matmul(A, S), q) 	
	return S, A, T

def Sign(**kwargs):
	'''
		i/p:
		msg: string, which the sender wants to brodcast
		A  : numpy array, Verification Key dimension nxm
		S  : numpy array, Signing key dimension mxk

		o/p:
		(z,c) : signature		
	'''	
	msg, A, S, q, n, m, k, d, sd, M = kwargs['msg'],kwargs['A'],kwargs['S'],kwargs['q'],kwargs['n'],kwargs['m'],kwargs['k'],kwargs['d'],kwargs['sd'],kwargs['M']	
	D = DiscreteGaussianDistributionLatticeSampler(ZZ**m, sd)
	count = 0
	while(True):
		y = np.array(D()) # discrete point in Zq^m
		c = util.hash_to_baseb(util.vector_to_Zq(np.matmul(A,y), q), msg, 3, k)  # 3 because we want b/w 0,1,2 small coefficients in Zq
		Sc = np.matmul(S,c)
		z = Sc + y #notice we didnt reduce (mod q)		
		try:					
			pxe = float(-2*z.dot(Sc) + Sc.dot(Sc))
			val = exp(pxe / (2*sd**2)) / M							
		except OverflowError:
			print "OF"			
			continue			
		if(random.random() < min(val, 1.0)):
			break
		if(count > 4): # beyond 4 rejection sampling iterations are not expected in general 
			raise ValueError("The number of rejection sampling iterations are more than expected")
		count += 1								
	return z, c

def Verify(**kwargs):
	'''
		Verification for the signature
		i/p:
		msg: the string sent by the sender
		(z,c): vectors in Zq, the signature
		A  : numpy array, Verification Key dimension nxm
		T : the matrix AS mod q ,it is used in the Verification of the signature
	'''
	msg, z, c, A, T, sd, eta, m, k, q = kwargs['msg'], kwargs['z'], kwargs['c'], kwargs['A'], kwargs['T'], kwargs['sd'], kwargs['eta'], kwargs['m'], kwargs['k'], kwargs['q']
	norm_bound = eta * sd * np.sqrt(m)
	# checks for norm of z being small and that H(Az-Tc mod q,msg) hashes to c
	vec = util.vector_to_Zq(np.array(np.matmul(A,z) - np.matmul(T,c)), q)
	hashedList = util.hash_to_baseb(vec, msg, 3, k)
	print hashedList, c 			
	if np.sqrt(z.dot(z)) <= norm_bound and np.array_equal(c, hashedList):
		return True
	else:
		return False

def testToy():
	
	#SIS parameters
	n, m, k, d, q = 128, 1000, 20, 1, 114356107 # these parameters must be carefully adjusted
	#n, m, k, d, q = 512, 8000, 80, 1, 114356107
	#b = 2*d + 1  # range for the Signing Key matrix
	M = 2.72   # the real value such that f(x) <= M * g(x), and an element from g(x) is accepted with probability f(x)/M*g(x)
	
	#Discrete Gaussian parameters
	#sd = 31495
	sd = 300	
	eta = 1.1

	#Computation
	S, A, T =  KeyGen(q = q,n = n,m = m,k = k,d = d)
	z, c = Sign(msg="hellohow", A = A, S = S, q = q, n = n, m = m, k = k, d = d, sd = sd, M = M)		
	print Verify(msg="hellohow", z = z, c = c, A = A, T = T, sd = sd, eta = eta, m = m,k = k, q = q)
	print Verify(msg="hellohow", z = z, c = c, A = A, T = T, sd = sd, eta = eta, m = m,k = k,q = q)
	print Verify(msg="Magoo", z = z, c = c, A = A, T = T, sd = sd, eta = eta, m = m,k = k,q = q)

testToy()