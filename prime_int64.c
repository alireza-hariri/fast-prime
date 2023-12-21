#include <stdio.h>
#include <stdlib.h>

#define N (10 * 1000 * 1000)

long long primes[N] = {2};
size_t primes_count = 1;

int is_prime(long long x)
{
    for (size_t i = 0; primes[i] * primes[i] <= x; ++i) {
        if (x % primes[i] == 0) {
            return 0;
        }
    }
    return 1;
}

int main(int argc, char *argv[])
{
    for (long long x = 3; primes_count < N; ++x) {
        if (is_prime(x)) {
            primes[primes_count++] = x;
        }
    }
    // printf("%d\n", primes[primes_count - 1]);
    printf("%lld\n", primes[primes_count - 1]);
    return 0;
}
