def product(l1,l2):
    prod = 1
    for c in range(len(l1)):
        prod = prod*(l1[c]**l2[c])
    return prod

def isprime(num):
    result = True if num % 2 != 0 and all(num % p != 0 for p in range(3, int(num ** 0.5) + 1, 2)) else False
    return result

def primefactors(m):
    p = m
    pf = []
    pm = []
    for j in range(2, p):
        cntr = 0
        while p % j == 0 and isprime(p) == False:
            cntr += 1
            p = int(p / j)
        if cntr > 0:
            pf.append(j)
            pm.append(cntr)
    if p in pf:
        pm[pf.index(p)] += 1
    elif p != 1:
        pf.append(p)
        pm.append(1)
    else:
        "Do Nothing"
    return pf, pm

def leastfactors(n):
    minf = []
    minm = []
    for i in range(2,n+1):
        a, b = primefactors(i)
        for f in a:
            if f not in minf:
                minf.append(f)
                minm.append(b[a.index(f)])
            elif minm[minf.index(f)] < b[a.index(f)]:
                minm[minf.index(f)] = b[a.index(f)]
            else:
                continue
    return product(minf, minm), minf, minm

print(leastfactors(20))