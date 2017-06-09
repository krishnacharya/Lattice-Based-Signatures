'''
Miscellanious utility functions
'''
from random import SystemRandom
import numpy as np
import hashlib as hl 
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
		to_integer_ring for each element in M a numpy array
	'''	
	for i in range(M.shape[0]):
		for j in range(M.shape[1]):
			M[i][j] = to_integer_ring(M[i][j], q)
	return M

def vector_to_Zq(v, q):
	'''
		to_integer_ring for each element in v a numpy array
	'''
	for i in range(len(v)):
		v[i] = to_integer_ring(v[i],q)
	return v

def crypt_secure_randint(r):
	'''
		input: 
		r : the range in which we want the random integer [0,r-1]
		output:
		a cryptographiically secure random integer in [0,r-1] 
	'''
	cryptogen = SystemRandom()  #takes entropy from operating system
	return cryptogen.randrange(0,r)		

def crypt_secure_matrix(r, n, m):
	'''	
		outputs: A numpy array with dimension nxm and integer elements in [0,r-1]
	'''
	return np.array([[crypt_secure_randint(r) for j in range(m)] for i in range(n)])	

def hash_to_baseb(matrix, message, b, k):
	'''
		i/p: 
			matrix : numpy array to be hashed
			message : string that the sender sends  

		o/p: 
			list with k elements each b/w 0 to b-1
	'''
	hexval = hl.sha512(np.array_str(matrix) + message).hexdigest() # returns a string with 128 hex digits
	return np.array(map(int, list(b2b(hexval, 16, b)[:k])))  # returns first k digits from hexval in a list

# this list of symbols allows conversion of numbers represented until base 36
base_symbols='0123456789abcdefghijklmnopqrstuvwxyz'

def v2r(n, b): # value to representation
    """Convert a positive number n to its digit representation in base b."""
    digits = ''
    while n > 0:
        digits = base_symbols[n % b] + digits
        n  = n // b
    return digits

def r2v(digits, b): # representation to value
    """Compute the number given by digits in base b."""
    n = 0
    for d in digits:
        n = b * n + base_symbols[:b].index(d)
    return n

def b2b(digits, b1, b2):
    """Convert the digits representation of a number from base b1 to base b2."""
    return v2r(r2v(digits, b1), b2)	

