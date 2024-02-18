from functools import lru_cache
from collections import Counter


@lru_cache(maxsize=None)
def computing(sequence):
    cnt = Counter(sequence)
    single = ''.join([k for k, v in cnt.items() if v == 1])
    return single

