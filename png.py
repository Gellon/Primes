# Prime Number Generator v1.0
import math
import sys

primes = [3]

if int(len(sys.argv) != 2) or int(sys.argv[1]) < 4:
    print("Use: png.py <NUMBER> \nFind all primes less than NUMBER.")
    sys.exit(-1)

print("#\t Prime")
print("1\t 2")
print("2\t 3")

for n in range(5, int(sys.argv[1]), 2):
    nn = math.trunc(math.sqrt(n))
    m = 0
    while primes[m] <= nn:
        if n % primes[m] == 0:
            break
        m += 1
    if primes[m] > nn:
        primes.append(n)
        print(len(primes) + 1, "\t", n)
#        print (n)
#print (f"Fonund: {len(primes) + 1} primes")
