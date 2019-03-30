def sumsandsquares(m):
    s1 = 0
    s2 = 0
    for i in range(1,m+1):
        s1+=i**2
        s2+=i
    return s2**2 - s1

print(sumsandsquares(100))
