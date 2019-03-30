def ispalindrome(n):
    l = int(len(str(n)) / 2) if len(str(n)) % 2 == 0 else int(len(str(n)) / 2) + 1
    return str(n)[:l] == str(n)[-l:][::-1]

ml = [x*y for x in range(100,1000) for y in range(100,1000) if ispalindrome(x*y)]

print(max(ml))