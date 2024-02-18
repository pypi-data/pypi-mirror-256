import tiktoken


def count_tokens(input_text):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(input_text))
