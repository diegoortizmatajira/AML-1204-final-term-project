def clean_title(title: str) -> str:
    if title:
        return title.replace('\n', '').replace('\t', '').replace('\r', '')[:64]
    else:
        return None
