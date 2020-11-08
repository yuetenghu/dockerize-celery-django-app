from typing import List, Dict, Union
import json
import pathlib

print(f"Current path: {pathlib.Path().absolute()}")

dists: List[List[int]] = [
    [0,  2,  9, 10],
    [1,  0,  6,  4],
    [15, 7,  0,  8],
    [6,  3, 12,  0]
]

with open("/app/data/dist_matrix/test.json", "w+") as f:
    json.dump(dists, f)
    print("Write finished")

with open("/app/data/dist_matrix/test.json", "r") as f:
    d: List[List[int]] = json.load(f)
    print("Reading now: =====")
    print(len(d))
    print(len(d[0]))
    print(d[1][2])

file_path: str = "/app/data/dist_matrix/sample_input.json"
with open(file_path, "r") as f:
    print(f" ===== Reading now: {file_path}  =====")
    t : Dict[str, List[Union[int, str]]] = json.load(f)
    print(t)

response_file_path: str = "/app/data/dist_matrix/sample_response.json"
with open(response_file_path, "r") as f:
    print(f" ===== Reading now: {file_path}  =====")
    r : Dict = json.load(f)
    print(r)
    print(r["rows"][0]["elements"][0]["duration"]["value"])