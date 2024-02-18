import os
import json


def list_samples(file_name: str) -> None:
    with open(file_name, "r") as f:
        data = json.load(f)
    data_sorted = sorted(
        data,
        key=lambda d : len(d["text"]),
        reverse=True
    )

    i = 0
    for d in data_sorted:
        print(len(d["text"]))
        i += 1
        if i > 50:
            break
