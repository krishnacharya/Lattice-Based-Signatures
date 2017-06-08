'''
Authors: Krishna Acharya, Dheeraj Pai, Sannidhya Shukla
Date:	7 June 2017
Brief Description:
Lattice Based Signature Based on the Fiat Shamir Framework
employs Unimodal Gaussian for Rejection sampling
based on Vadim Lyubachevsky's Eurocrypt 2012 paper.
Parameters of the signature scheme are based on SIS q,n,m,d
'''
import numpy as np
import random_gen as rg
n,m,k,d,q = 512,8786,80,1,134217757
# q is a prime of order 2^27

def to_integer_ring(ele, q):
	'''
		input:
		q: 	 is a prime of polynomial size
		ele: integer to be reduced mod q to the range [-(q-1)/2,(q-1)/2]
			 such that it still belongs to the same congruence modulo class
		output:
			element in the ring Zq
	'''
	return (ele % q) if (ele % q <= (q-1)/2) else (ele % q) - q

def matrix_to_Zq(M, q):
	'''
		to_integer_ring of each element in M a numpy array
	'''	
	for i in range(M.shape[0]):
		for j in range(M.shape[1]):
			M[i][j] = to_integer_ring(M[i][j], q)
	return M						

def KeyGen():
	'''
		input:
		q : polynomial size prime number
		n, m, k : dimensions specifiers
		d : SIS parameter, hardest instances are where d ~ q^(n/m)
		d < q
		output:
		Signing Key S :  Matrix of dimension mxk with coefficients in [-d.d]
		Verification Key A : Matrix of dimension nxm with coefficients from [-(q-1)/2,(q-1)/2]
		T : the matrix AS ,it is used in the Verification of the signature

	'''
	global n,m,k,d,q
	S = rg.crypt_secure_matrix(d, m, k)
	A = rg.crypt_secure_matrix((q-1)/2, n, m)
	T = matrix_to_Zq(np.matmul(A, S), q)	
	return S, A, T

print KeyGen()[0]

def Sign():
	pass

def Verify():
	pass		