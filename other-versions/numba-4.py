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

MAX_INT_64 = np.iinfo(np.int64).max
NOT_CALCULATED = MAX_INT_64 - 1 # NOT_CALCULATED flag


@njit()
def get_primes_v3(primes_arr, n_primes, primes_power2_arr, from_n, to_n):
    assert from_n % 2 == 0
    for i in range(from_n + 1, to_n, 2):
        for j in range(n_primes):
            if i % primes_arr[j] == 0:
                break
            if i <= primes_power2_arr[j]:
                if primes_power2_arr[j] == NOT_CALCULATED:
                    primes_power2_arr[j] = primes_arr[j] ** 2
                    if (
                        i > primes_power2_arr[j]
                    ):  # power2 condition was fake (and it was happend because pow2 was not calculated)
                        continue
                primes_arr[n_primes] = i
                n_primes += 1
                if n_primes >= N:
                    return n_primes
                break
    return n_primes


initial_primes = np.array(initial_primes, dtype=np.int32)
primes_arr = np.ones(10_000_000 + 100, dtype=np.int32) * -1
primes_power2_arr = np.ones(10_000_000 + 100, dtype=np.int64) * NOT_CALCULATED

n_primes = initial_primes.shape[0]
primes_arr[:n_primes] = initial_primes
primes_power2_arr[:n_primes] = initial_primes**2

start = CHUNK_SIZE
end = start + CHUNK_SIZE * 10
for _ in tqdm(range(200_000_000//CHUNK_SIZE//10)):
    n_primes = get_primes_v3(primes_arr, n_primes, primes_power2_arr, start, end)
    start = end
    end = start + CHUNK_SIZE * 10
    if n_primes >= N:
        break

print(time.time() - t0)
print(primes_arr[10_000_000 - 1])
