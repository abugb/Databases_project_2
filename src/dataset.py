DATASET_PATH = "Project2Dataset"

def block_path(file_num: int) -> str:
    return f"{DATASET_PATH}/F{file_num}.txt"

def read_first_record(file_num: int) -> bytes:
    with open(block_path(file_num), "rb") as file:
        return file.read(40)

def random_value(record: bytes) -> int:
    return int(record[33:37])

def read_records():
    for file_num in range(1, 100):
        with open(block_path(file_num), "rb") as file:
            block = file.read()
        for offset in range (0, len(block), 40):
            record = block[offset:offset + 40]
            yield file_num, offset, record, random_value(record)

def read_indexed_records(locations):
    offsets_by_file = {}
    for file_num, offset in locations:
        offsets_by_file.setdefault(file_num, []).append(offset)

    records = []
    for file_num, offsets in offsets_by_file.items():
        with open(block_path(file_num), "rb") as file:
            for offset in offsets:
                file.seek(offset)
                records.append(file.read(40))

    return records, len(offsets_by_file)