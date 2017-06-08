'''
	This module provides cryptographiically secure random numbers and matrices
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
		outputs: A numpy array with dimension nxm and integer elements in [-r,r]
	'''
	return np.array([[crypt_secure_randint(r) for j in range(m)] for i in range(n)])