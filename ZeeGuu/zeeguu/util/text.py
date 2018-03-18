import regex


def split_words_from_text(text):
    words = regex.findall(r'(\b\p{L}+\b)', text)
    return words