from dataset import read_records
from math import ceil, floor

def build_indexes():
    hash_idx = {}
    array_idx = [[] for _ in range(5000)]
    for file_num, offset, _, random_v in read_records():
        location = (file_num, offset)
        hash_idx.setdefault(random_v, []).append(location)
        array_idx[random_v - 1].append(location)
    return hash_idx, array_idx

def range_locations(array_idx, lower, upper):
    last_value = len(array_idx)
    if lower >= last_value or upper <= 1:
        return []

    first = floor(max(lower, 0)) + 1
    last = ceil(min(upper, last_value + 1)) - 1

    locations = []
    for value in range(first, last + 1):
        locations.extend(array_idx[value - 1])
    return locations