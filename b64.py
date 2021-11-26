import string

b64_symbols = "".join([
    string.digits,
    string.ascii_uppercase,
    string.ascii_lowercase,
    "+/"
])

def to_base64(n: int):
    # Only intended for upto 4096 using main app
    i, j = divmod(n, 64)
    return f"{b64_symbols[i] if i else ''}{b64_symbols[j]}"

if __name__ == "__main__":
    print(to_base64(100))