def shorten_text(text: str, length: int = 80) -> str:
    if len(text) > length:
        return text[0:length] + "..."
    return text
