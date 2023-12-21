
from tqdm import tqdm
import numpy as np
import math 
import time

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
N = 10_000_000


def check_condidats(condidats, primes_arr):
    """ 
      check divisibility of an array of number with array of primes 
      returns an array of numbers with no factor as new condidats
    """
    # a factor have zero modulo => all non-zero modulo means no factor found
    no_factor = (condidats.reshape(-1,1) % primes_arr.reshape(1,-1)).all(1)
    return condidats[no_factor]



def prime_chunk_generator(biggerst_num , primes):
    """
      primes: array of sorted primes to be chunked
      biggerst_num: biggest number that we want to check for primality
    """
    size=3
    start=0
    while True:
        chunk = primes[start:start+size]
        start = start+size
        if size<150:
            size *= 3
        if chunk[-1]**2 < biggerst_num:
            yield chunk
        else:
            yield chunk[chunk**2 <= biggerst_num]
            break


def get_primes(condidats, primes_arr):
    max_condid = condidats[-1]
    max_prime = primes_arr[-1]
    assert int(max_prime)**2 > max_condid

    for chunk in prime_chunk_generator(max_condid,primes_arr):
        condidats = check_condidats(condidats, chunk)
    return condidats



primes_arr = np.array(initial_primes,dtype=np.int32)
primes_buffer = [] # list of prime arrays
# chunk_i=1
prime_cnt = len(primes_arr)
for chunk_i in tqdm(range(1,200_000_000//CONDIDATE_CHUNK)):
    condidats = np.arange(chunk_i*CONDIDATE_CHUNK+1,(chunk_i+1)*CONDIDATE_CHUNK,2)
    if int(primes_arr[-1])**2 < condidats[-1]:
        primes_arr = np.concatenate([primes_arr,*primes_buffer])
        primes_buffer = []
    new_primes = get_primes(condidats, primes_arr)
    primes_buffer.append(new_primes)
    prime_cnt += len(new_primes)
    if prime_cnt >= N :
        break

print(time.time() - t0)
print(np.concatenate([primes_arr,*primes_buffer])[N-1])

