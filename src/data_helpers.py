def split_amr_sent(amrstring):
    strings = amrstring.split("\n")
    amr = "\n".join([l for l in strings if not l.startswith("#")])
    sent = amrstring.split("::snt ")[1].split("\n")[0]
    return amr, sent

def read_amr_file(p):
    """reads linearized string amr graphs from amr sembank.
    
    Args:
        p (list): path to AMR sembank that contains AMR graphs, i.e.
                                # ::snt ...
                                (x / ...
                                    :a (...))

                                # ::snt ...
                                (...

    Returns:
        - list with string AMRs in Penman format
    """

    with open(p) as f:
        amrs = [l for l in f.read().split("\n\n") if l]
    tmp = [split_amr_sent(string) for string in amrs]
    amrs = [x[0] for x in tmp]
    sents = [x[1] for x in tmp]
    amrs = [amr for amr in amrs if amr]
    sents = [sent for sent in sents if sent]
    assert len(amrs) == len(sents)
    return amrs, sents

def read_score_file(p):
    with open(p) as f:
        scores = [float(s) for s in f.read().split("\n")]
    return scores

def write_string_to_file(string, p):
    with open(p, "w") as f:
        f.write(string)

