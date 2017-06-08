import base_conv as bc
import numpy as np
import hashlib as hl
def hash_to_baseb(matrix, message, b, k):
	'''
		i/p: 
			matrix : numpy array to be hashed
			message : string that the sender sends  

		o/p: 
			list with k elements each b/w 0 to b-1
	'''
	hexval = hl.sha512(np.array_str(matrix) + message).hexdigest() # returns a string with 128 hex digits
	return bc.b2b(hexval, 16, b)[:k]
