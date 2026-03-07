from data import read_file


def analyze_text(filepath: str):
    text = read_file(filepath)

    lines = text.count("\n") + 1 if text else 0
    words = len(text.split())
    characters = len(text)

    return {
        "lines": lines,
        "words": words,
        "characters": characters
    }