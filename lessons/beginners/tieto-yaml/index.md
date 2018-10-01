## YAML

YAML is a data serialisation language designed to be directly writable and readable by humans.


It’s a strict superset of JSON, with the addition of syntactically significant newlines and indentation, like Python. Unlike Python, however, YAML doesn’t allow literal tab characters for indentation.

Install **pyyaml** package:

```
pip install pyyaml
```

Example Python script:

```
import yaml

sample_yaml_as_dict = '''
first_dict_key: some value
second_dict_key: some other value
'''

sample_yaml_as_list = '''
- list item 1
- list item 2
'''

my_config_dict = yaml.load(sample_yaml_as_dict)
print(my_config_dict)

my_config_list = yaml.load(sample_yaml_as_list)
print(my_config_list)
```

Output:

```
python python_yaml.py
{'first_dict_key': 'some value', 'second_dict_key': 'some other value'}
['list item 1', 'list item 2']
```

