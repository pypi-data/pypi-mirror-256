"""
Module for handling CSV files.
"""


def convert(data):
    """
    Convert data to CSV format.

    Args:
        data (list): The data to be converted to CSV format.

    Returns:
        str: The data in CSV format.
    """
    csv_data = ''
    for row in data:
        csv_data += ','.join([str(value) for value in row]) + '\n'
    return csv_data


def opformat(file_path):
    """
    No formatting needed for CSV files.

    Args:
        file_path (str): The path to the CSV file to be formatted.
    """
    pass  # No formatting needed for CSV files
