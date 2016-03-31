"""Basic Data reading and writing utility, stores data as JSON files."""

import json


def readFile(filepath):
    """Attempt to read a JSON file from the given filepath.

    Keyword Arguments:
    filepath -- Path to the file to read.

    Returns:
    dict or bool -- The JSON dictionary if successful, False otherwise.

    """
    try:
        with open(filepath, encoding="utf-8", mode="r") as reading_file:
            return json.loads(reading_file.read())
    except OSError:
        return False


def writeFile(filepath, data):
    """Attempt to write given data as JSON to the given filepath.

    Keyword Arguments:
    filepath -- Path to the file to write to.
    data -- Data to write as JSON to the file.

    Returns:
    bool -- True if successful, False otherwise.

    """
    try:
        with open(filepath, encoding="utf-8", mode="w") as writing_file:
            writing_file.write(json.dumps(data,
                                          indent=4,
                                          sort_keys=True,
                                          separators=(',', ' : ')))
        return True
    except OSError:
        return False
