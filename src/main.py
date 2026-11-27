import sys
from decimal import Decimal
from dataset import read_indexed_records, read_records
from time import perf_counter
from indexes import build_indexes, range_locations

READY_MSG = "Program is ready and waiting for user command."

EQUALITY = "SELECT * FROM Project2Dataset WHERE RandomV = "
RANGE = "SELECT * FROM Project2Dataset WHERE RandomV > "
RANGE_SEPARATOR = " AND RandomV < "
INEQUALITY = "SELECT * FROM Project2Dataset WHERE RandomV != "
CREATE_INDEX = "CREATE INDEX ON Project2Dataset (RandomV)"

def table_scan(matches):
    records = []
    files_read = set()
    for file_num, _, record, random_v in read_records():
        files_read.add(file_num)
        if matches(random_v):
            records.append(record)
    return records, len(files_read)

def run_query(lookup, lookup_method=None):
    start = perf_counter()
    records, file_count = lookup()
    elapsed_ms = (perf_counter() - start) * 1000

    for record in records:
        print(record.decode("ascii"))
    if lookup_method is not None:
        print(f"Lookup method: {lookup_method}")
    print(f"Elapsed time: {elapsed_ms:.3f} ms")
    print(f"Data files read: {file_count}")

def run_scan(matches, lookup_method=None):
    run_query(lambda: table_scan(matches), lookup_method)

def main():
    hash_idx = None
    array_idx = None
    print(READY_MSG)
    for line in sys.stdin:
        command = line.strip()
        if command == CREATE_INDEX:
            hash_idx, array_idx = build_indexes()
            print("The hash-based and array-based indexes are built successfully.")
        elif command.startswith(EQUALITY):
            value = Decimal(command[len(EQUALITY):])
            if hash_idx is None:
                run_scan(lambda random_v: random_v == value, "Table Scan")
            else:
                run_query(
                    lambda: read_indexed_records(hash_idx.get(value, [])),
                    "Hash-based Index",
                )
        elif command.startswith(RANGE):
            bounds = command[len(RANGE):]
            lower_text, upper_text = bounds.split(RANGE_SEPARATOR, maxsplit=1)
            lower = Decimal(lower_text)
            upper = Decimal(upper_text)
            if array_idx is None:
                run_scan(lambda random_v: lower < random_v < upper, "Table Scan")
            else:
                run_query(
                    lambda: read_indexed_records(
                        range_locations(array_idx, lower, upper)
                    ),
                    "Array-based Index",
                )
        elif command.startswith(INEQUALITY):
            value = Decimal(command[len(INEQUALITY):])
            run_scan(lambda random_v: random_v != value)
        print(READY_MSG)

if __name__ == "__main__":
    main()