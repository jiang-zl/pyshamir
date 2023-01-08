from pyshamir.shamirSecretShare import ShamirShareSecret
from pyshamir.addictiveSecretShare import AddSecretShare

w_len, c_len = 5, 3


def get_shares(share: list, weight: list, add_sharing: AddSecretShare):
    for w_idx in range(w_len):
        share[w_idx] = add_sharing.sharing(weight[w_idx], c_len)


def aggregator(res: list, shares: list, add_sharing: AddSecretShare) -> list:
    # c_len is equal to len(shares)
    for s_idx in range(c_len):
        for c_idx in range(c_len):
            for w_idx in range(w_len):
                res[w_idx] = (res[w_idx] + shares[s_idx][w_idx][c_idx]) % add_sharing.mod_q


if __name__ == '__main__':
    weights = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15]
    ]

    sharing = AddSecretShare(128)

    share1 = [[0] * c_len for _ in range(w_len)]
    share2 = [[0] * c_len for _ in range(w_len)]
    share3 = [[0] * c_len for _ in range(w_len)]

    get_shares(share1, weights[0], sharing)
    get_shares(share2, weights[1], sharing)
    get_shares(share3, weights[2], sharing)

    agg = [0] * w_len
    aggregator(agg, [share1, share2, share3], sharing)
    print(agg)

    # test of shamir secret sharing
    # shamirSS = ShamirShareSecret(256, 10, 6)
    # coefs    = shamirSS.Init(283451145) # input the secret to sharing
    # print("The coefficients of polynomial is {}".format(coefs))
    # shares   = shamirSS.Sharing(coefs)
    # print("The shares of secret is ")
    # for idx in range(len(shares)):
    #     print("({}, {})".format(shares[idx][0], shares[idx][1]))
    # secret   = shamirSS.Reconstruct(shares)
    # print("The result of reconstruction is {}".format(secret))
