"""
Module for handling XML files.
"""

import xml.dom.minidom as minidom


def convert(data):
    """
    Convert data to XML format.

    Args:
        data (dict): The data to be converted.

    Returns:
        str: The data in XML format.
    """
    xml_data = '<?xml version="1.0" ?>\n<root>'
    for key, value in data.items():
        if isinstance(value, list):  # Si el valor es una lista, iteramos sobre sus elementos
            for item in value:
                xml_data += '  <item>'
                if isinstance(item, dict):  # Si el elemento es un diccionario, representamos cada par clave-valor
                    for k, v in item.items():
                        xml_data += f'    <{k}>{v}</{k}>'
                else:  # Si el elemento no es un diccionario, lo representamos como está
                    xml_data += f'    <{key}>{item}</{key}>'
                xml_data += '  </item>'
        else:  # Si el valor no es una lista, lo representamos como está
            xml_data += f'  <{key}>{value}</{key}>'
    xml_data += '</root>'
    return xml_data


def opformat(file_path):
    """
    Format an XML file to make it more readable.

    Args:
        file_path (str): The path to the XML file to be formatted.
    """
    try:
        with open(file_path, 'r') as file:
            xml_str = file.read() # Read file
            xml = minidom.parseString(xml_str) # Parse content xml
            with open(file_path, 'w') as file: # Open file as writing
                file.write(xml.toprettyxml(indent="  \t")) # format file
    except FileNotFoundError:
        print(f"Failed to format XML file: {file_path}")
