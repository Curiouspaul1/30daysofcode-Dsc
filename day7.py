def fibgen(a):
    """
        fibgen is a function that spits out the x-term of the famous
        fibonacci sequence.
        arg: x, --> fibgen(x) --> x-term:
        e.g 7, --> fibgen(7) --> 13
    """

    seq = [0,1]
    while len(seq) <= a:
        # sum up last two terms
        next_ = seq[len(seq)-1] + seq[len(seq)-2]
        seq.append(next_)
    return seq[a]

print(fibgen(7))
