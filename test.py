A = 0
B = 1
C = 1

while C > 0.01:
    value = (C * A) + ((1-C) * B)
    print(value)
    C /= 1.2