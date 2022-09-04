def division(x, y):
    return abs(x) if int(y) == 0 else abs(x)/abs(y)


def sum_digits(x):
    return sum(c.isdigit() for c in str(x))