# Using (slightly modified) sieve of Eratosthenes to generate primes (rather than trial division) for efficiency.
# I originally tried to write this starting with array of all #s 2 to n, and then actually remove the composite
# numbers (as shown in code snippit below:
#       myList = list(range(3, n, 2))
#       i = 0
#       while myList[i] < n ** (1 / 2) + 1:
#           myList = [x for x in myList if x not in list(range(myList[i] ** 2, n, 2 * myList[i]))]
#           i += 1
# But, I found this to run too slow and reverted to using memory to indicate which indices (for odd #s 2 through n)
# were determined composite (index value = False) or prime (index value = True).  While it's still essentially
# the same method, this memory way ran much faster.

def generatePrimesUpTo(n):
    myList = [True]*(n+1)   # index i represents value = 2*i+1 (all odds up to n)
    for i in range(2, int(n ** 0.5) + 1):
        myList[i**2:n+1:i] = [False]*(int(n/i)-i+1)
    return [i for i,x in enumerate(myList) if x is True and i not in [0,1]]

print(sum(generatePrimesUpTo(2000000)))