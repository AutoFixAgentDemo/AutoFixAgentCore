import json

import demjson3 as demjson
from ..logs import logger


def validate_json(data):
    """
    demjson is a very flexible JSON parser and generator that can handle loose JSON formats,
    such as those with trailing commas, single-quoted strings.

    Validate if the input data is in JSON format. If it can be parsed correctly, return the parsed object;
    if it cannot be parsed correctly, return None.

    :param data: Input data, can be a string or a dictionary.
    :return: Parsed object or None.
    """
    try:
        # Attempt to parse the input data
        parsed_data = demjson.decode(data)
        return json.dumps(parsed_data)
    except demjson.JSONDecodeError as e:
        # If parsing fails, return None
        logger.error(f"Error decoding JSON: {e}\n {data}")

        return None


def check_msg(context):
    try:
        data = json.loads(context)
        if data["Comments About the Patch"] in ["Accept", "accept"]:
            return True
        else:
            return False
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
    return False
