from typing import List
import math

def get_prime_factor(n):
    factor = []
    root = int(math.sqrt(n))
    while(n % 2 == 0):
        factor.append(2)
        n //= 2
        
    for i in range(3, root+1, 2):
        while(n % i == 0):
            factor.append(i)
            n //= i
    if n > 2: 
        factor.append(n)
    return factor

def smallest_prime_value(n: int) -> int:
    # Plan:
    # For each number, get prime factors, then recursively combine factors
    factor = get_prime_factor(n)
    
    # edge cases prevent infinite recursion
    if len(factor) == 1 or sum(factor) == n:
        return n
    return smallest_prime_value(sum(factor))
    
    

# R E A D M E
# DO NOT CHANGE the code below, we use it to grade your submission.
# If changed, your submission will be failed automatically.
if __name__ == '__main__':
    n = int(input())
    print(smallest_prime_value(n))
