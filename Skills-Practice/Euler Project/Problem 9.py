# Efficiency method:  generate primitive triple using Euclid's formula (defined below),
#                     then check if there is a positive integer number multiple m such that m*(a+b+c) = n,
#                     continue to loop through this process until above condition is met.
# Euclid's Formula: For positive integers m > n, a = m^2 - n^2, b = 2mn, c = m^2 + n^2 creates a pythagorean triple.
#                   Furthermore, the triple is primitive (GCF of a, b, c = 1) if and only if m and n are coprime and
#                   exactly one is odd.


def PythagoreanTripletProduct(pySum):
    for m in range(2, int(pySum/3)):
        # "a" must be less than pySum/2 because a must be less than c.
        #     We don't know whether a < or > b in this method.
        #     Otherwise we could restrict further to pySum/3 if we knew a < b < c).
        # Therefore, m^2 - n^2 < pySum/2. Solving this is how we get n_lower as the lower bound of n.
        n_lower = (int((m**2 - pySum/2)**(1/2)) if m**2 > pySum/2 else 1) + (1 if m % 2 == 1 else 0)
        for n in range(n_lower, m, 2):
            a = m**2 - n**2
            b = 2*m*n
            c = m**2 + n**2
            f = pySum / (a + b + c)
            if f == int(f):
                result = a*b*c*f**3
                break
    return result

print(PythagoreanTripletProduct(1000))