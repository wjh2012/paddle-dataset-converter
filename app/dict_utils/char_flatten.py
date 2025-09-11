import json


def main(flatten_map, input_str):
    inv = {}
    for base, variants in flatten_map.items():
        if not isinstance(variants, (list, tuple)):
            continue
        for v in variants:
            inv[v] = base
    translate_table = {ord(k): v for k, v in inv.items() if len(k) == 1}
    res = input_str.translate(translate_table)
    for k in sorted((k for k in inv if len(k) > 1), key=len, reverse=True):
        res = res.replace(k, inv[k])
    return res


if __name__ == "__main__":
    flatten_map_path = "../../charset/char_map.json"
    input_char = "￣.″“）"

    with open(flatten_map_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)
    result = main(mapping, input_char)
    print(result)
