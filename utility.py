def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def to_generator(iterable):
    for i in range(0, len(iterable)):
        yield i