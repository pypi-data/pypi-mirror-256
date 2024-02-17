#!/usr/bin/env python3
import string


def col_num_to_letter(col_num):
    s = ''

    # If num_cols is 0 or less, return empty
    if col_num <= 0:
        return s

    # Start at 0
    num = col_num - 1
    # divide num by 26
    # if >= 1, then we have 1 or more letters in front
    # if < 1, then we compute the current letter
    divisor = num // 26
    if divisor >= 1:
        s = col_num_to_letter(divisor) + s

    return s + string.ascii_uppercase[num % 26]


if __name__ == '__main__':
    pass