import os
from urllib.parse import urlparse

import requests

res = requests.get("https://vulzap.github.io/data/blacklist.json")
BLACKLIST: list = res.json().get("blacklist")


def is_same_origin(source: str, target: str) -> bool:
    source_domain = ".".join(urlparse(url=source).netloc.split(".")[-2:])
    target_domain = ".".join(urlparse(url=target).netloc.split(".")[-2:])

    return source_domain == target_domain


def is_blacklist(url: str) -> bool:
    ext = (os.path.splitext(url)[1])[1:]

    if ext in BLACKLIST:
        return True

    return False


def pattern_create(length: int):
    pattern = ""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars_lower = chars.lower()
    digits = "0123456789"

    while len(pattern) < length:
        for c in chars:
            for cl in chars_lower:
                for d in digits:
                    if len(pattern) < length:
                        pattern += c + cl + d
                    else:
                        break
                if len(pattern) >= length:
                    break
            if len(pattern) >= length:
                break

    return pattern[:length]


def pattern_offset(pattern: str, result: str) -> int:
    offset = pattern.find(result)

    if offset != -1:
        return offset + len(result)
    else:
        return


if __name__ == "__main__":
    pattern = pattern_gen(100)
    print(pattern)
    print(pattern_offset(pattern, "A0"))
