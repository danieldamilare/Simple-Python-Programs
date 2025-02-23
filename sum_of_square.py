import math 

def find_sum(n):
    """
    return the number of triplet that satisfy the constrant: the sum of
    the square of the smallest two number is equal to the square of the 
    largest number
    Examples
    >>> find_sum(10)
        4
    #[(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10)]
    """
    #loop to 4 as no number between 1 and 4 satisfy the condition
    result = 0
    for i in range(n, 4, -1):
        for j in range(i):
            square_root  = math.sqrt(i * i - j * j)
            if square_root - int(square_root) == 0 and square_root < i:
                print(i, j, square_root, end="\t")
                result += 1
    return result
