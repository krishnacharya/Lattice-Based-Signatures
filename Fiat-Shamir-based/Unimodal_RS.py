'''
Authors: Krishna Acharya, Dheeraj Pai, Sannidhya Shukla
Date:	7 June 2017
Brief Description:
Lattice Based Signature Based on the Fiat Shamir Framework
employs Unimodal Gaussian for Rejection sampling
based on Vadim Lyubachevsky's Eurocrypt 2012 paper.
Parameters of the signature scheme are based on SIS q,n,m,d
'''
from random import SystemRandom
import numpy as np
def crypt_secure_randint(r):
	'''
		input: 
		r : the range in which we want the random integer [-r,r]
		output:
		a cryptographiically secure random integer in [-r,r] 
	'''
	cryptogen = SystemRandom()  #takes entropy from operating system
	return cryptogen.randrange(-r,r+1)

def crypt_secure_matrix(r, n, m):
	'''	
		outputs: A matrix with dimension nxm and integer elements in [-r,r]
	'''
	return np.matrix([[crypt_secure_randint(r) for j in range(m)] for i in range(n)])

def hash_to_ternary():
	pass	

def KeyGen(n, m, k, d, q):
	'''
		input:
		q : polynomial size prime number
		n, m, k : dimensions specifiers
		d : SIS parameter, hardest instances are where d ~ q^(n/m)

		output:
		Signing Key S :  Matrix of dimension mxk with coefficients in [-d.d]
		Verification Key A : Matrix of dimension nxm with coefficients from [-(q-1)/2,(q-1)/2]
		T : the matrix AS ,it is used in the Verification of the signature

	'''
	S = crypt_secure_matrix(d, m, k)
	A = crypt_secure_matrix((q-1)/2, n, m)
	T = np.matmul(A, S)
	return S, A, T

def Sign():
	pass

def Verify():
	pass		