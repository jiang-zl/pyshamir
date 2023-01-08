import random
from .secretShareUtil import getprimeover, invert

try:
    import gmpy2
    HAVE_GMP = True
except ImportError:
    HAVE_GMP = False

try:
    from Crypto.Util import number
    HAVE_CRYPTO = True
except ImportError:
    HAVE_CRYPTO = False

class ShamirShareSecret:
    """Contains a prime q and Init, Sharing, Reconstruct methods

    Args:
        qsize (int): the size of the Zq.
        n    (int) : the number of secret shares,
        t    (int) : the number of threshold.
        
    Attributes:
        q (int): the modulus of all parameters,
        n (int): as above,
        t (int): as above.
    
    Methods:
        Init(input s)                     : return the coefficients of polynomial (coefs),
        Sharing(input [coefs])            : return secret shares (i, f(i)),
        Recon(input [(i, f(i))], input t) : return the secret (s).
    
    Private Method:
        GetPolynomialValue(input idx, input coefs) : return the value of f(idx)

    """

    def __init__(self, qsize, n, t):
        self.n = n
        self.t = t
        self.q = getprimeover(qsize)
    
    def __GetPolynomialValue(self, idx, coefs):
        if len(coefs) != self.t:
            raise ValueError("Error: the number of coef is not equal to t(threshold)")
        var, res = 1, 0
        for coef in coefs:
            res = (res + var * coef % self.q) % self.q
            var = (var * idx) % self.q
        return res
    
    def Init(self, s):
        coefs = [s]
        for i in range(1, self.t):
            coefs.append(random.SystemRandom().randrange(3, self.q))
        return coefs
    
    def Sharing(self, coefs):
        shares = []
        for i in range(1, self.n + 1):
            val = self.__GetPolynomialValue(i, coefs)
            shares.append((i, val))
        return shares
    
    def Reconstruct(self, shares):
        if len(shares) < self.t:
            raise ValueError("Error: the number of shares must large than t(threshold)")
        res = 0
        for i in range(0, self.t):
            tmp1, muls = 1, 1
            curId, curVal = shares[i][0], shares[i][1]
            for j in range(0, self.t):
                if curId == shares[j][0]:
                    continue
                tmp1 = tmp1 * (-shares[j][0]) % self.q
                muls = muls * (curId - shares[j][0]) % self.q
            tmp2 = invert(muls, self.q)
            curVal = curVal * tmp1 * tmp2 % self.q
            res = (res + curVal) % self.q
        return (res % self.q)
