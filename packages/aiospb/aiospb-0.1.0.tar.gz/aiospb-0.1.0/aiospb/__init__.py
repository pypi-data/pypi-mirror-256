import time


def get_timestamp() -> int:
    return int(time.time() * 1000)
