import argparse
import math

def get_prime_factors(n):
    #we try until find the root from n
    limit = int(math.sqrt(n)) + 1

    #we try odd numbers
    for i in range(3, limit, 2):
        if n % i == 0:
            p = i
            q = n // i
            return p, q
    return None, None

def main ():
    # read the args on the console
    parser = argparse.ArgumentParser(description='Crack RSA')
    parser.add_argument('-e', type=int, required=True, help='Public exponent')
    parser.add_argument('-n', type=int, required=True, help='Modulus')
    parser.add_argument('--ciphertext', type=int, required=True, help='Cipher Text')

    args = parser.parse_args()

    e = args.e
    n = args.n
    c = args.ciphertext

    #factorize n to find p and q
    p,q = get_prime_factors(n)

    if p is None:
        return

    #calculates phi(n)
    phi = (p-1) * (q-1)

    d = pow(e, -1, phi)

    #finds the message
    message = pow(c, d, n)
    print(message)

if __name__ == '__main__':
    main()