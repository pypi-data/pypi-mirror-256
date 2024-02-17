import time

import flower_crane
from py_flower_crane.meeting import find_meeting
from py_flower_crane.util import get_data

N = 100


def bench_flower_crane():
    data = get_data()
    data = (
        [(el[0], el[1]) for el in data[0]],
        [(el[0], el[1]) for el in data[1]],
        data[2].tolist(),
        data[3].tolist(),
        data[4].tolist(),
        data[5].tolist(),
        data[6],
        data[7],
    )

    start = time.time()
    for _ in range(N):
        _ = flower_crane.find_meeting(*data)
    end = time.time()
    print(f"Rust: {N} iterations in {end-start:.2f} seconds")


def bench_flower_crane_np():
    data = get_data()
    start = time.time()
    for _ in range(N):
        _ = flower_crane.find_meeting_np(*data)
    end = time.time()
    print(f"Rust Numpy: {N} iterations in {end-start:.4f} seconds")


def bench_py_flower_crane():
    data = get_data()
    start = time.time()
    for _ in range(N):
        _ = find_meeting(*data)
    end = time.time()
    print(f"Python: {N} iterations in {end-start:.2f} seconds")


if __name__ == "__main__":
    bench_py_flower_crane()
    bench_flower_crane()
    bench_flower_crane_np()
