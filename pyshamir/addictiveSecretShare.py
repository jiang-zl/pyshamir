import random
from pyshamir.secretShareUtil import getprimeover


class AddSecretShare:
    def __init__(self, sec_lvl):
        self.mod_q = getprimeover(sec_lvl)

    def sharing(self, secret: int, count: int) -> list:
        if count < 2:
            raise Exception("Number of parties is less than 2.")
        ret, cnt = [], 0
        for i in range(count - 1):
            cur = random.SystemRandom().randrange(3, self.mod_q)
            cnt = (cnt + cur) % self.mod_q
            ret.append(cur)
        cur = ((secret - cnt) % self.mod_q + self.mod_q) % self.mod_q
        ret.append(cur)
        return ret

    def recon(self, shares: list) -> int:
        if len(shares) < 2:
            raise Exception("Length of shares is less than 2.")
        secret = 0
        for sh in shares:
            secret = (secret + sh) % self.mod_q
        return secret % self.mod_q
