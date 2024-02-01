
## prime-benchmark <i>(Python vs C)</i>

inspired by [this repoistory](https://github.com/tsoding/prime-benchmark), here I conducted a basic performance comparison betweenand C and Python with the same task. the task is to find first 1e+7 primes.

### final results
| code | Machine-1 Runtime | Machine-2 Runtime |
|:--------------: |:--------------:| :--------------:|
| prime-int32.c | 36s (24s with -O3) | 56s (37s with -O3) |
| prime-int64.c | 50s (42s with -O3) | ~2 min |
| dummy-prime.py | > 24 hour | > 24 hour |
| simple-prime.py | ~30 min | ~25 min|
| numpy-prime.py | 77s (65s int32) | ~3.5 min |
| numba-prime.py | 30s | 51s |

### bonus solution
| code | Machine-1 Runtime | Machine-2 Runtime |
|:--------------: |:--------------:| :--------------:|
| parallel-prime.py | 9.7s | 3.1s |

### conclusion
on both machines namba code was able to beat c/c++ (g++ compiled) in 64-bit calculations (with or without -O3 option), and it was also able to beat g++ without -O3 option in the 32-bit calculations

### deeper questions:
    1- what makes the diffrent of -O3 option? 
    2- why in64 calculations affect c++ that much but it barely affect numba runtime (kind of 1% at most)?
    3- why my economic core-i5 is faster than the Hi-end 64-core Xeon in this benchmark (when its pluged in)
    4- what makes the diffrent of LLVM compiled (I mean numba) and g++ compiled runtime
    
