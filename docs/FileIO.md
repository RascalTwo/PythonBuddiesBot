##FileIO.py

A very minimal file loading-saving utility file. Uses JSON to load and save python dictionaries for long-term storage.

##Code Walkthrough

```Python
import json
```

Import [json](https://docs.python.org/3/library/json.html).

Used to read and save dictionaries to the files.

```Python
def readFile(filepath):
    with open(filepath, encoding="utf-8", mode="r") as reading_file:
        return json.loads(reading_file.read())
```

The `read_file` method.

Used to read a file at the given filepath and return the dictionary-representation of the JSON data within it.

This may throw an `OSError` if the given file does not exist, so beware.

```Python
def write_file(filepath, data):
    with open(filepath, encoding="utf-8", mode="w") as writing_file:
        writing_file.write(json.dumps(data,
                                      indent=4,
                                      sort_keys=True,
                                      separators=(',', ' : ')))
```

The `write_file` method.

Used to write dictionary-data as json to the file at the given filepath.