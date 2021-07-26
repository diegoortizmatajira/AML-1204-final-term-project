def clean_value(value: str) -> str:
    return value.replace('\n', '').replace('\t', '').replace('\r', '')


def get_random_chars(chars: str, length: int) -> str:
    return ''


def get_random_alphanumeric(length: int) -> str:
    return get_random_chars('abcdefghijklmnopqrstuvwxyz0123456789', length)


def get_random_numeric(length: int) -> str:
    return get_random_chars('0123456789', length)


def generate_identifier(name: str) -> str:
    value = clean_value(name)
    return name
