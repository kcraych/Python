def isprime(n):
    for i in range(2, n + 1):
        if n % i == 0:
            break
        else:
            continue
    return i == n if n > 2 else 3 == n

def largestprimefactor(m):
    if isprime(m):
        pf = [m]
    else:
        p = m
        pf = []
        for j in range(2, p):
            if p % j == 0:
                p = int(p / j)
                pf.append(j)
                if isprime(p):
                    pf.append(p)
                    break
                else:
                    continue
            else:
                continue
    return max(pf)

print(largestprimefactor(600851475143))