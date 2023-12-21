"""
  using pure python to find first 1e+7 primes 
"""
from tqdm import tqdm
primes=[2]
powers=[4]
TARGET = 10_000_000
for i in tqdm(range(3,200_000_000,2)):
    for prime,po in zip(primes,powers):
        if not i%prime:
            break         
        if i<po:
            primes.append(i)
            powers.append(i*i)
            break 
    else:
        raise Exception("unexpected error.")
    if len(primes) == TARGET:
                break
print(primes[TARGET-1])