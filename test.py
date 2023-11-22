
def lerp():
    A = 0
    B = 1
    C = 1

    value = (C * A) + ((1-C) * B)
    C /= 1.2
    yield value

print(next(lerp()))
print(next(lerp()))