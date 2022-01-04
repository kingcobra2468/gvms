def exp_sequence():
    """Initiates generator for exponential sequence 2^n.
    """
    seq = 1

    while True:
        seq <<= 1
        yield(seq)
