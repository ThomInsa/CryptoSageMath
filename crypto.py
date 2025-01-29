import time
import random
from sympy import nextprime, factorint, gcd
import matplotlib.pyplot as plt
import seaborn as sns

def my_gcd(a, b):
    while b != 0:
        tmp = b
        b = a % b
        a = tmp
    return a

def my_xgcd(a, b):
    u0, u1 = 1, 0
    v0, v1 = 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return a, u0, v0

def my_pow(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

def my_is_prime(n):
    if n < 2:
        return False
    for a in [2, 3, 5, 7]:
        if a >= n:
            break
        if my_pow(a, n - 1, n) != 1:
            return False
    return True

def my_next_prime(n):
    while True:
        n += 1
        if my_is_prime(n):
            return n

def rsa_gen(l):
    p = nextprime(random.getrandbits(l))
    q = nextprime(random.getrandbits(l))
    N = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = pow(e, -1, phi)
    return (e, N), d

def rsa_enc(e, N, M):
    return my_pow(M, e, N)

def rsa_dec(d, N, C):
    return my_pow(C, d, N)

def eg_set(l):
    q = nextprime(random.getrandbits(l))
    p = 2 * q + 1
    while not my_is_prime(p):
        q = nextprime(random.getrandbits(l))
        p = 2 * q + 1
    g = 2
    while my_pow(g, q, p) == 1:
        g += 1
    return q, p, g

def eg_gen(q, p, g):
    sk = random.randint(2, q - 1)
    pk = my_pow(g, sk, p)
    return sk, pk

def eg_enc(q, p, g, pk, M):
    k = random.randint(2, q - 1)
    c1 = my_pow(g, k, p)
    c2 = (M * my_pow(pk, k, p)) % p
    return c1, c2

def eg_dec(q, p, g, sk, C):
    c1, c2 = C
    s = my_pow(c1, sk, p)
    M = (c2 * pow(s, -1, p)) % p
    return M

def test_factor():
    l = 8
    bit_sizes = []
    times = []
    while l <= 111:
        rq = random.randrange(2, 2**l)
        q = nextprime(rq)
        rp = random.randrange(2, 2**l)
        p = nextprime(rp)
        N = p * q
        start = time.time()
        factorint(N)
        stop = time.time()
        bit_sizes.append(l)
        times.append((stop - start) * 10**6)
        print(l, (stop - start) * 10**6)
        l += 1

    sns.set_theme(style='darkgrid')
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=bit_sizes, y=times, marker='o')
    plt.xlabel('Taille des facteurs (bits)')
    plt.ylabel('Temps d’exécution (μs)')
    plt.title('Temps d’exécution de factorint en fonction de la taille des facteurs')
    plt.show()
