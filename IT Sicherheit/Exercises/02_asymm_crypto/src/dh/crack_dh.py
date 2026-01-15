import argparse

def solve_log (g, target, n):

    # we try every possible number from 1 to n
    for x in range(1,n):
        #we do pow(base, exponent, modulo) to make (g**x) % n
        if pow(g, x, n) == target:
            return x
    return None

def main ():

    #read the args on the console
    parser = argparse.ArgumentParser(description='Crack Diffie-Hellman')
    parser.add_argument('-g', type=int, required=True, help='Generator')
    parser.add_argument('-n', type=int, required=True, help='Modulus')
    parser.add_argument('--alice', type=int, required=True, help='Alice public value')
    parser.add_argument('--bob', type=int, required=True, help='Bob public value')

    args = parser.parse_args()

    g= args.g
    n= args.n
    A= args.alice
    B= args.bob

    #we look for 'a' so: g^a % n == A

    a_private = solve_log (g, A, n)

    if a_private == None:
        print('No private key found')
        return

    #we look for 'K' s K = B^a % n
    shared_K = pow(B, a_private, n)

    print(shared_K)

if __name__ == '__main__':
    main()



