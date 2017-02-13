from yaml import safe_load


def read_yaml(filename):
    """How to read yaml file."""
    with open(filename, encoding='utf-8') as file:
        data = safe_load(file)
    return data
