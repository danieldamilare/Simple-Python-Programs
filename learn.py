#!/usr/bin/python3
import sys

def fibonacci(num):
    a,b, i = 0, 1, 0

    while i < num//2:
        print(a, b, end = " ")
        a, b = a + b, a + 2 * b
        i+=1

    if(num & 1):
        print(a, end = " ")
    

    return a

def standard_arg(arg):
    print(arg)

def pos_only_arg(arg, /):
    print(arg)

def kwd_only_arg(*, arg ):
    print(arg)


def sum(*numbers):
    sum = 0;
    for i in numbers:
        sum += i
    print("sum: ", sum, end =" ")


def concat(sep=" ", *arg):
        return sep.join(map(str, arg))

if __name__ == '__main__':
    if(len(sys.argv) > 1):
        fibonacci(int(sys.argv[1]))
    sum(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    print("Trying standard_arg with position only")
    standard_arg(20)
    print("Trying standard_arg with keyword")
    standard_arg(arg=20)
    print("Trying pos_only_arg with position only")
    pos_only_arg(20)
    print("Trying kwd_only_arg with position only")
    kwd_only_arg(arg=20)
    print(eval(concat(" * ", 1, 2, 3, 4, 5, 6, 7, 8)))
    dan, joseph = [1, 2]
