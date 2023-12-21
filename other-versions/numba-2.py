from numba import njit
from tqdm import tqdm
import numpy as np
import time
import math 

t0 = time.time()

CONDIDATE_CHUNK = 5000

primes = []
for i in range(2,CONDIDATE_CHUNK):
    for prime in primes:
        if i%prime == 0:
            break
    else:
        primes.append(i)
initial_primes = primes


@njit()
def get_primes_v2(condidats, primes_arr):
    max_condid = condidats[-1]
    max_prime = primes_arr[-1]
    assert int(max_prime)**2 > max_condid
    # prime_pow2 = primes_arr**2
    is_prime = np.ones(condidats.shape[0],dtype=np.bool8)
    for i in range(condidats.shape[0]):
        for j in range(primes_arr.shape[0]):
            if condidats[i] % primes_arr[j] == 0 :
                is_prime[i] = False 
                break
            if j%4 == 0: 
                if  condidats[i] <= primes_arr[j]**2:
                    break 
    return condidats[is_prime]


primes_arr = np.array(initial_primes,dtype=np.int64)
primes_buffer = [] # list of prime arrays
# chunk_i=1
prime_cnt = len(primes_arr)
for chunk_i in tqdm(range(1,100000)):
    condidats = np.arange(chunk_i*CONDIDATE_CHUNK+1,(chunk_i+1)*CONDIDATE_CHUNK,2)
    if int(primes_arr[-1])**2 < condidats[-1]:
        primes_arr = np.concatenate([primes_arr,*primes_buffer])
        primes_buffer = []
    new_primes = get_primes_v2(condidats, primes_arr)
    primes_buffer.append(new_primes)
    prime_cnt += len(new_primes)
    if prime_cnt >= 10_000_000:
        break

print(time.time() - t0)
print(np.concatenate([primes_arr,*primes_buffer])[10_000_000-1])
