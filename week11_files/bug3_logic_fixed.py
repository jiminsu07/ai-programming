
def find_max(scores):
    biggest = scores[0]
    for i in range(1, len(scores)):
        if scores[i] > biggest:
            biggest = scores[i]
    return biggest


def count_pass(scores, cutoff=60):
    n = 0
    for s in scores:
        if s >= cutoff:
            n += 1
    return n

