from sage.all import *
from sage.stats.distributions.discrete_gaussian_lattice import DiscreteGaussianDistributionLatticeSampler
import hashlib
import random

# security parameters
n = 256
m = 1000
q = 7681
sd = 300
eta = 1.1
alpha = 1
k = 12
M = 3.0
In = matrix.identity(n)
D = DiscreteGaussianDistributionLatticeSampler(ZZ**m, sd)

def H(x, y):
    seed = 0
    while True:
        w = 0
        out = vector([0]*n)
        h = int(hashlib.sha512(str((x, y, seed))).hexdigest(), 16)
        while h != 0:
            i = h % n
            h /= n
            if out[i] != 1:
                out[i] = 1
                w += 1
            if w == k:
                return out
        seed += 1

def KeyGen():
    Aq_ = random_matrix(Zmod(q), n, m-n)
    S_ = matrix(Zmod(q), m-n, n, lambda i, j: choice(range(0, 2**(alpha+1))))
    #Aq = Aq_.augment((-Aq_)*S_)
    S = (S_.stack(In)).change_ring(Zmod(2*q))
    _Aq_ = Aq_.change_ring(ZZ)
    _S_ = S_.change_ring(ZZ)
    A = (2*_Aq_).augment(q*In - 2*_Aq_*_S_).change_ring(Zmod(2*q))
    return (A, S)

def Sign(msg, A, S):
    while True:
        y = vector(D())
        Ay = A*y.change_ring(Zmod(2*q))
        c = H(Ay, msg)
        b = choice([0, 1])
        Sc = S.change_ring(ZZ)*c
        z = y + (-1)**b*Sc
        prob =exp(float(Sc.norm()**2)/2*sd**2)/(M*math.cosh(z*Sc/sd**2))
        if random.random() < prob:
            return (z, c)

def Verify(msg, A, sign):
    z, c = sign
    B2 = eta*sd*math.sqrt(m)
    if z.norm() > B2:
        return False
    if max(z) >= float(q)/4:
        return False
    if H(A*z + q*c, msg) == c:
        return True
    return False
    

def main():
    pk, sk = KeyGen()
    m1 = "Hello, Alice. This is Bob."
    m2 = "Hello, Alice. This is Eve."
    s = Sign(m1, pk, sk)
    print Verify(m1, pk, s) # should print True
    print Verify(m2, pk, s) # should print False

if __name__ == "__main__":
    main()
