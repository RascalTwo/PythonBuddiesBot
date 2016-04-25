"""Basic Data reading and writing utility, stores data as JSON files."""

import json


def read_file(filepath):
    """Attempt to read a JSON file from the given filepath, may raise exception.

    Keyword Arguments:
    filepath -- Path to the file to read.

    Returns:
    dict -- The JSON dictionary.

    """
    with open(filepath, encoding="utf-8", mode="r") as reading_file:
        return json.loads(reading_file.read())


def write_file(filepath, data):
    """Attempt to write given data as JSON to the given filepath.

    Keyword Arguments:
    filepath -- Path to the file to write to.
    data -- Data to write as JSON to the file.

    """
    with open(filepath, encoding="utf-8", mode="w") as writing_file:
        writing_file.write(json.dumps(data,
                                      indent=4,
                                      sort_keys=True,
                                      separators=(',', ' : ')))
