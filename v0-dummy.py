from tqdm import tqdm
primes = []
TARGET = 10_000_000
for i in tqdm(range(2,200_000_000)):
    for prime in primes:
        if i%prime == 0:
            break
    else:
        primes.append(i)
    if len(primes) == TARGET:
        break
print(primes[TARGET-1])