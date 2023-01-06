from pyshamir.shamirScheme import ShamirShareSecret

if __name__ == '__main__':
    shamirSS = ShamirShareSecret(256, 10, 6)
    coefs    = shamirSS.Init(283451145) # input the secret to sharing
    print("The coefficients of polynomial is {}".format(coefs))
    shares   = shamirSS.Sharing(coefs)
    print("The shares of secret is ")
    for idx in range(len(shares)):
        print("({}, {})".format(shares[idx][0], shares[idx][1]))
    secret   = shamirSS.Reconstruct(shares)
    print("The result of reconstruction is {}".format(secret))
