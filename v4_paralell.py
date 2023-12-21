from numba import njit
from tqdm import tqdm
import numpy as np
import time
import math
from joblib import Parallel, delayed

t0 = time.time()
INIT_RANGE = 15000
initial_primes = [2]
for i in range(3, INIT_RANGE, 2):
    for prime in initial_primes:
        if i % prime == 0:
            break
        if i <= prime**2:
            initial_primes.append(i)
            break
    else:
        raise Exception("unexpected!")


N = 10_000_000


@njit(nogil=True)
def get_primes_v4(primes_in, primes_out, n_prime, from_n, to_n):
    assert from_n % 2 == 0
    for i in range(from_n + 1, to_n, 2):
        for j in range(len(primes_in)):
            if i % primes_in[j] == 0:
                break 
            if i <= primes_in[j] ** 2:
                primes_out[n_prime] = i
                n_prime += 1
                break
    return n_prime


MAX_CHECK = 200_000_000
WORKER_CHUNK = INIT_RANGE * 10
MAIN_CHUNK = INIT_RANGE * 100


initial_primes = np.array(initial_primes, dtype=np.int64)
assert MAX_CHECK < initial_primes[-1] ** 2


def find_primes_work(from_n, to_n, initial_primes):
    n = math.ceil((to_n - from_n) / WORKER_CHUNK)
    # allocate memory for results 
    primes_out = np.zeros(MAIN_CHUNK//10, dtype=np.int64) 
    n_prime = 0
    for i in range(n):
        start = WORKER_CHUNK * i + from_n
        end = min(start + WORKER_CHUNK, to_n)
        n_prime = get_primes_v4(initial_primes, primes_out, n_prime, start, end)
    return primes_out[:n_prime]


# mesure compile time
t1 = time.time()
buffer = np.zeros(10, dtype=np.int64)
get_primes_v4(initial_primes[:100], buffer, 0, INIT_RANGE, INIT_RANGE+10)
print("compile time",time.time() - t1)


jobs = []
from_n = INIT_RANGE
n = math.ceil((MAX_CHECK-INIT_RANGE)/MAIN_CHUNK)
for i in range(n):
    to_n = min(from_n + MAIN_CHUNK,MAX_CHECK)
    jobs.append(delayed(find_primes_work)(from_n, to_n, initial_primes))
    from_n = to_n


with Parallel(n_jobs=7,verbose=5,backend='threading') as parallel:
    results = parallel(jobs)


print(time.time() - t0)
print(np.concatenate([initial_primes,*results])[N - 1])
