seq = [1,2]
c = 1
s = 2
while seq[c]+seq[c-1] < 4000000:
    seq.append(seq[c]+seq[c-1])
    c += 1
    s += seq[c] if seq[c] % 2 == 0 else 0

print(s)