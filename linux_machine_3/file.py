#!/usr/bin/env python3

import ast

def collect_hex_strings(obj):
    """
    Recursively traverse a nested list structure and collect any strings
    that start with '0x' (hexadecimal notation). Return them in the
    order they appear.
    """
    result = []
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, list):
                # Recurse into nested lists
                result.extend(collect_hex_strings(item))
            elif isinstance(item, str) and item.startswith("0x"):
                # Found a hex string like '0x70'
                result.append(item)
    return result

def main():
    # Read the scrambled data from out.txt
    with open("out.txt", "r") as f:
        contents = f.read()

    # Safely parse the Python-like list structure
    scrambled_data = ast.literal_eval(contents)

    # Collect all "0xNN" strings in a depth-first manner
    hex_codes = collect_hex_strings(scrambled_data)

    # Convert each hex string to its ASCII character
    decoded_chars = [chr(int(code, 16)) for code in hex_codes]

    # Join them into the final flag
    flag = "".join(decoded_chars)

    print(flag)

if __name__ == "__main__":
    main()
