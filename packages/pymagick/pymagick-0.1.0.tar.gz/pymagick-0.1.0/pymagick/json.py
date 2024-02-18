"""
Module for handling JSON files.
"""

import json


def convert(data):
    """
    Convert data to JSON format.

    Args:
        data (dict or list): The data to be converted to JSON format.

    Returns:
        str: The data in JSON format.
    """
    return json.dumps(data)


def opformat(file_path):
    """
    Format a JSON file to make it more readable.

    Args:
        file_path (str): The path to the JSON file to be formatted.
    """
    try:
        with open(file_path, 'r') as file:
            parsed_json = json.load(file)
        with open(file_path, 'w') as file:
            json.dump(parsed_json, file, indent=4)  # Format JSON with indentation
    except (ValueError, FileNotFoundError):
        print(f"Failed to format JSON file: {file_path}")
