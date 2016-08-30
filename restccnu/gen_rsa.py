# coding: utf-8

"""
    gen_rsa.py
    ``````````

    key, secret = gen_rsa(num1, num2)
"""

import random


def gcd(n1, n2):
    # n1 > n2
    if n2 == 0:
        return n1
    else: return gcd(n2, n1 % n2)
    

def ext_gcd(n1, n2):
    # 扩展欧几里德算法
    # 求最大公约数的同时, 求满足贝组公式的可能解
    if n2 == 0:
        return 1, 0, n1
    else:
        x, y, q = ext_gcd(n2, n1 % n2)
        x, y = y, ( x - (n1 // n2) * y)
        return x, y, q


def is_coprime(n1, n2):
    if gcd(n1, n2) == 1:
        return True
    else: return False


def gen_rsa(num1, num2):
    """
    key, secret = gen_rsa(num1, num2)
    open key, keep secret
    """
    n = num1 * num2
    pi_n = (num1-1) * (num2-1)
    e = random.randint(1, pi_n)
    while not is_coprime(pi_n, e):
        e = random.randint(1, pi_n)
    # 扩展欧几里德算法求模反元素d的可能解
    x, y, q = ext_gcd(e, pi_n)
    d = x
    # key: (n,e) secret (n, d)
    return ((n, e), (n, d)) 


if __name__ == '__main__':
    key, secret = gen_rsa(61, 53)
    print '''
        key => %s
        secret => %s
    ''' % (key, secret)
