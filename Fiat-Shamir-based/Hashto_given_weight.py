import hashlib

def hash_Dk(s):
	'''
		securely hashes a string s to a length k (= 512) string with 
		64(kappa) many +-1 's.
		This can be extended to other lengths and kappa's. 
		it would be bitwise operations on the binary value of a 
		suitable hash
	'''
	oparray = [0] * 512
	num = bin(int(hashlib.sha256(s).hexdigest(),16))[2:]
	i = 0
	j = 0
	while(i < 256):
		shift8 = int(num[i+1 : i+4], 2)
		if(num[i] == '0'):
			oparray[j + shift8] = 1
		else:
			oparray[j + shift8] = -1
		
		j += 8
		i += 4
			
	return oparray

def test():
	s = 'Call me Ishmael.'
	print hash_Dk(s)	
