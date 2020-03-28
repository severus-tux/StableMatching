import random
import math
import itertools

# this only works for Iterable[Iterable]
def is_latin_rectangle(rows):
    valid = True
    for row in rows:
        if len(set(row)) < len(row):
            valid = False
    if valid and rows:
        for i, val in enumerate(rows[0]):
            col = [row[i] for row in rows]
            if len(set(col)) < len(col):
                valid = False
                break
    return valid

def is_latin_square(rows):
    return is_latin_rectangle(rows) and len(rows) == len(rows[0])

# : prepare the input
n = 9
items = list(range(1, n + 1))
# shuffle items
random.shuffle(items)
# number of permutations
print(math.factorial(n))


def latin_square1(items, shuffle=True):
    result = []
    for elems in itertools.permutations(items):
        valid = True
        for i, elem in enumerate(elems):
            orthogonals = [x[i] for x in result] + [elem]
            if len(set(orthogonals)) < len(orthogonals):
                valid = False
                break
        if valid:
            result.append(elems)
    if shuffle:
        random.shuffle(result)
    return result

rows1 = latin_square1(items)
for row in rows1:
    print(row)
print(is_latin_square(rows1))


def latin_square2(items, shuffle=True, forward=False):
    sign = -1 if forward else 1
    result = [items[sign * i:] + items[:sign * i] for i in range(len(items))]
    if shuffle:
        random.shuffle(result)
    return result

rows2 = latin_square2(items)
for row in rows2:
    print(row)
print(is_latin_square(rows2))

rows2b = latin_square2(items, False)
for row in rows2b:
    print(row)
print(is_latin_square(rows2b))