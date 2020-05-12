"""Quickly generates a random integer, via a generator"""

from random import randint
import numpy as np


def gen_on_the_fly(n):
    numbers = np.arange(n, dtype=np.uint32)
    for i in range(n):
        j = randint(i, n-1)
        numbers[i], numbers[j] = numbers[j], numbers[i]
        yield numbers[i]


if __name__ == '__main__':
    for num in gen_on_the_fly(100000000):
        print(num)
