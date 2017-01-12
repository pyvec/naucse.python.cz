from yaml import safe_load


# How to read yaml file.
def read_yaml(filename):
    with open(filename, encoding='utf-8') as file:
        data = safe_load(file)
    return data
