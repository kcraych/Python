def generateprimes(m):
    primes = [2]
    i = 3
    while len(primes) < m:
        primes.append(i) if all(i%j != 0 for j in primes if j <= (i**0.5)+1) else "Do Nothing" # does this still loop through all i%j cases or does it exit as false as soon as it finds an i%j == 0 case?
        i += 2
    return primes

print(max(generateprimes(10001)))