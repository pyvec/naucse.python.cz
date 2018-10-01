## JSON

In Python, the json module provides an API similar to convert in-memory Python objects to a serialized representation known as JavaScript Object Notation (JSON) and vice-a-versa.

### Encode Python objects as JSON strings

```
json.dump(obj, fp,
                  skipkeys=False,
                  ensure_ascii=True,
  		  check_circular=True,
		  allow_nan=True,
		  cls=None,
		  indent=None,
		  separators=None,
		  default=None,
		  sort_keys=False, **kw)
```

The above method serialize obj as a JSON formatted stream to fp (a .write()-supporting file-like object) using the following conversion table.

```
Python											JSON
dict											object
list, tuple										array
str												string
int, float, int- & float-derived Enums			number
True											true
False											false
None											null
```

### Python Dictionaries to JSON strings

```
import json
student = {"101":{"class":'V', "Name":'Rohit',  "Roll_no":7},
           "102":{"class":'V', "Name":'David',  "Roll_no":8},
           "103":{"class":'V', "Name":'Samiya', "Roll_no":12}}
print(json.dumps(student));
```

Output:

```
{"103": {"class": "V", "Name": "Samiya", "Roll_no": 12}, 
"102": {"class": "V", "Name": "David", "Roll_no": 8}, 
"101": {"class": "V", "Name": "Rohit", "Roll_no": 7}}
```

### Python Dictionaries to JSON strings (sorted by key)

```
import json
student = {"101":{"class":'V', "Name":'Rohit',  "Roll_no":7},
           "102":{"class":'V', "Name":'David',  "Roll_no":8},
           "103":{"class":'V', "Name":'Samiya', "Roll_no":12}}
print(json.dumps(student, sort_keys=True));
```

Ooutput:

```
{"101": {"Name": "Rohit", "Roll_no": 7, "class": "V"}, 
"102": {"Name": "David", "Roll_no": 8, "class": "V"}, 
"103": {"Name": "Samiya", "Roll_no": 12, "class": "V"}}
```

### Python tuple to JSON array

```
import json
tup1 = 'Red', 'Black', 'White';
print(json.dumps(tup1));
```

Output:

```
["Red", "Black", "White"]
```

### Python list to JSON array

```
import json
list1 = [5, 12, 13, 14];
print(json.dumps(list1));
```

Output:

```
[5, 12, 13, 14]
```

### Python string to JSON string

```
import json
string1 = 'Python and JSON';
print(json.dumps(string1));
```

Output:

```
"Python and JSON"
```

### Python int, float, int- & float-derived Enums to JSON number

```
import json
x = -456;
y = -1.406;
z =  2.12e-10
print(json.dumps(x));
print(json.dumps(y));
print(json.dumps(z));
```

Output:

```
-456
-1.406
2.12e-10
```

### Decode JSON strings into Python objects

Basic usage:

```
json.load(fp, 
          cls=None, 
		  object_hook=None, 
		  parse_float=None, 
		  parse_int=None, 
		  parse_constant=None, 
		  object_pairs_hook=None, **kw)
```

```
JSON				Python
object				dict
array				list
string				str
number (int)		int
number (real)		float
true				True
false				False
null				None
```

### JSON strings to Python Dictionaries

```
import json
json_data = '{"103": {"class": "V", "Name": "Samiya", "Roll_n": 12}, "102": {"class": "V", "Name": "David", "Roll_no": 8}, "101": {"class": "V", "Name": "Rohit", "Roll_no": 7}}';
print(json.loads(json_data));
```

Output:

```
{"103": {"class": "V", "Name": "Samiya", "Roll_no": 12}, 
"102": {"class": "V", "Name": "David", "Roll_no": 8}, 
"101": {"class": "V", "Name": "Rohit", "Roll_no": 7}}
```

### Python list to JSON array

```
import json
list1 = '[ "Ford", "BMW", "Fiat" ]'
print(json.loads(list1));
```

### JSON string to Python string

```
import json 
Json_string = "Python and JSON" 
print(json.dumps(Json_string));
```

Output:

```
"Python and JSON"
```
