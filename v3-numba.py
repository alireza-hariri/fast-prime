from numba import njit
from tqdm import tqdm
import numpy as np
import time
import math

t0 = time.time()

CHUNK_SIZE = 5000

primes = []
for i in range(2, CHUNK_SIZE):
    for prime in primes:
        if i % prime == 0:
            break
    else:
        primes.append(i)

initial_primes = primes
N = 10_000_000


@njit()
def get_primes_v3(primes_arr, n_primes, from_n, to_n):
    assert from_n % 2 == 0
    for i in range(from_n + 1, to_n, 2):
        for j in range(n_primes):
            if i % primes_arr[j] == 0:
                break
            if i <= primes_arr[j]**2:
                primes_arr[n_primes] = i
                n_primes += 1
                if n_primes > N:
                    return n_primes
                break
    return n_primes


initial_primes = np.array(initial_primes, dtype=np.int64)
primes_arr = np.ones(N + 100, dtype=np.int64) * -1

n_primes = initial_primes.shape[0]
primes_arr[:n_primes] = initial_primes

start = CHUNK_SIZE
end = start + CHUNK_SIZE*10
for _ in tqdm(range(200_000_000//CHUNK_SIZE//10)):
    n_primes = get_primes_v3(primes_arr,n_primes,start,end)
    start = end
    end = start + CHUNK_SIZE*10
    if n_primes >= N:
        break

print(time.time() - t0)
print(primes_arr[N - 1])
