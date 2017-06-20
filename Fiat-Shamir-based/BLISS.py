'''
Integer Ring Version of BLISS
Author: Krishna Acharya, Sannidhya Shukla, Dheeraj Pai 
'''
import util
import numpy as np
from sage.all import *
from sage.stats.distributions.discrete_gaussian_lattice import DiscreteGaussianDistributionLatticeSampler
from math import exp
import random
import hashlib
from numpy import linalg as LA

def hash_iterative(s, n, k):
	'''
	Uses Hashing technique mentioned in BLISS pg 19
	i/p: string s to be hashed to binary string of length n and weight k
	'''	 
	i = 0 # seed which increases till we get Bk^n
	while(True):
		Bk = [0] * n
		I_val = int(hashlib.sha512(s + str(i)).hexdigest(), 16)
		count = 0
		while(I_val > 0):
			pos = I_val % n
			I_val /= n
			if(Bk[pos] == 0):
				Bk[pos] = 1
				count += 1
			if(count == k):
				return np.array(Bk)
		i += 1	

def KeyGen(**kwargs):
	'''
	Appendix B of BLISS paper
	m_bar = m + n

	o/p:	
	A: Public Key n x m' numpy array
	S: Secret Key m'x n numpy array
	'''
	q, n, m, alpha = kwargs['q'], kwargs['n'], kwargs['m'], kwargs['alpha']
	Aq_bar = util.crypt_secure_matrix(-(q-1)/2, (q-1)/2, n, m)
	S_bar = util.crypt_secure_matrix(-(2)**alpha, (2)**alpha, m, n) # alpha is small enough, we need not reduce (modq)
	S = np.vstack((S_bar, np.eye(n, dtype = int))) # dimension is m_bar x n, Elements are in Z mod(2q)
	A = np.hstack((2*Aq_bar, q * np.eye(n, dtype = int) - 2*np.matmul(Aq_bar,S_bar))) # dimension is n x m_bar , Elements are in Z mod(2q)
	#return util.matrix_to_Zq(A, 2*q), S, Aq_bar, S_bar
	return util.matrix_to_Zq(A, 2*q), S

def KeyGen_test():
	A, S, Aq_bar, S_bar = KeyGen(q = 7,n = 5, m = 7, alpha=1)
	print Aq_bar
	print S_bar
	print A
	print S
	print np.matmul(A,S) - 7*np.eye(5, dtype=int)

def Sign(**kwargs):
	'''
	Algorithm 1, Pg 12 of BLISS paper
	o/p:
	z,c 
	'''
	msg, A, S, m, n, sd, q, M, kappa = kwargs['msg'], kwargs['A'], kwargs['S'], kwargs['m'], kwargs['n'], kwargs['sd'], kwargs['q'], kwargs['M'], kwargs['kappa']
	m_bar = m + n
	D = DiscreteGaussianDistributionLatticeSampler(ZZ**m_bar, sd)
	count = 0
	while(True):
		y = np.array(D()) # m' x 1 
 		reduced_Ay = util.vector_to_Zq(np.matmul(A, y), 2*q)
		c = hash_iterative(np.array_str(reduced_Ay) + msg, n, kappa) # still not the hash but this is test run		
		b = util.crypt_secure_randint(0, 1)
		Sc = np.matmul(S,c)
		z = y + ((-1)**b) * Sc
		try:			
			exp_term = exp(float(Sc.dot(Sc)) / (2*sd**2))
			cosh_term = np.cosh(float(z.dot(Sc)) / (sd**2))
			val = exp_term / (cosh_term * M)				
		except OverflowError:
			print "OF"			
			continue			
		if(random.random() < min(val, 1.0)):
			break
		if(count > 10): # beyond 4 rejection sampling iterations are not expected in general 
			raise ValueError("The number of rejection sampling iterations are more than expected")
		count += 1								
	return z, c

def Verify(**kwargs):
	msg, A, m, n, sd, q, eta, z, c, kappa = kwargs['msg'], kwargs['A'], kwargs['m'], kwargs['n'], kwargs['sd'], kwargs['q'], kwargs['eta'], kwargs['z'], kwargs['c'], kwargs['kappa']
	B2 = eta*sd*np.sqrt(m)
	reduced_prod = util.vector_to_Zq(np.matmul(A,z) + q*c, 2*q)
	#print np.sqrt(z.dot(z)),B2
	#print LA.norm(z,np.inf),float(q)/4
	if np.sqrt(z.dot(z)) > B2  or LA.norm(z,np.inf) >= float(q)/4:		
		return False	
	if np.array_equal(c, hash_iterative(np.array_str(reduced_prod)+msg, n, kappa)):
		return True
	return False

def test():
	# Classical SIS parameters
	n, m, alpha, q = 128, 872, 1, 114356107
	kappa = 20
	
	#Discrete Gaussian Parameters
	sd = 300
	eta = 1.2

	A, S = KeyGen(q = q,n = n,m = m,alpha = alpha)
	#print np.array(np.matmul(A,S) - q*np.eye(n),dtype=float)/(2*q) #to test AS = q mod(2q)
	z, c = Sign(msg = "Hello Bob",A = A,S = S,m = m,n = n,sd = sd,q = q,M = 3.0,kappa = kappa)
	print z
	print c
	print Verify(msg = "Hello Bob", A=A, m=m, n=n, sd=sd, q=q, eta=eta, z=z, c=c, kappa = kappa)
	print Verify(msg = "Hello Robert", A=A, m=m, n=n, sd=sd, q=q, eta=eta, z=z, c=c, kappa = kappa)
	print Verify(msg = "Hello Roberto", A=A, m=m, n=n, sd=sd, q=q, eta=eta, z=z, c=c, kappa = kappa)
	print Verify(msg = "Hola Roberto", A=A, m=m, n=n, sd=sd, q=q, eta=eta, z=z, c=c, kappa = kappa)

test()