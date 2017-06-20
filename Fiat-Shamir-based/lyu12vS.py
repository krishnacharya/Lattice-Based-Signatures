'''
Implementation of Lyubachevsky's Eurocrypt 2012 paper in Sage
'''

from sage.all import *
from sage.stats.distributions.discrete_gaussian_lattice import DiscreteGaussianDistributionLatticeSampler
import random
import hashlib

#SIS parameters
n = 128 
q = 114356107
d = 1
k = 20
m = 1000
M = 2.7

b = 2*d + 1
#discrete Gaussian
sd = 300
eta = 1.1
D = DiscreteGaussianDistributionLatticeSampler(ZZ**m, sd)

def H(x):
    # random oracle
    h = int(hashlib.sha512(str(x)).hexdigest(), 16)
    out = vector([0]*k, Zmod(q))
    for i in range(0, k) :
        out[i] = h%b
        h /= b
        i += 1
    return out

def gen():
    S = matrix(Zmod(q), m, k, lambda i, j: choice(range(0, b)))
    A = random_matrix(Zmod(q), n, m)
    T = A*S

    sk = S
    vk = (A, T)
    
    return (sk, vk)

def sign(msg, A, S):
    count = 0
    while True:
        count+=1
        if count == 1e3:
            return (0, 0)
        y = vector(D())
        Ay = A*y.change_ring(Zmod(q))
        c = H((Ay, msg))
        Sc = S.change_ring(ZZ)*c.change_ring(ZZ)
        z = Sc + y
        pxe = float(-2*z*Sc + (Sc.norm())**2)
        if random.random() < exp(pxe/(2*(sd**2)))/M:
            return (z,c)

def verify(msg, z, c, A, T): 
    if z.norm() <= eta*sd*sqrt(m) and c == H((A*z-T*c, msg)):
        return True
    return False

sk, vk = gen()
z, c = sign("Longer Message than the previous one.", vk[0], sk)
print verify("Longer Message than the previous one.", z, c, vk[0], vk[1])
print verify("long msg than the previous 1.", z, c, vk[0], vk[1])
