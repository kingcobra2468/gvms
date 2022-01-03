def exp_sequence():
    seq = 1

    while True:
        seq <<= 1
        yield(seq)
