#!/usr/bin/env python3
import ast

def collect_hex_strings(obj):
    result = []
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, list):
                result.extend(collect_hex_strings(item))
            elif isinstance(item, str) and item.startswith("0x"):
                result.append(item)
    return result

def main():
    with open("out.txt", "r") as f:
        data = ast.literal_eval(f.read())
    hexes = collect_hex_strings(data)
    flag = "".join(chr(int(h,16)) for h in hexes)
    print(flag)

if __name__ == '__main__':
    main()
