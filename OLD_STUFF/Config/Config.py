import configparser
import os
from configparser import SafeConfigParser


class Section:
    """
    Class to allow treating the sections in the config as an attribute
    """
    def __init__(self, values):
        self.__dict__.update(values)


class Config:
    """
    Class to access config values.
    """
    def __init__(self, file_path):
        # Parse the config file
        parser = SafeConfigParser()
        parser.optionxform = str
        found = parser.read(file_path)
        
        # Ensure the config file was parsed
        if not found:
            raise ValueError("Unable to read the config file!")

        # Loop through the sections
        for section in parser.sections():
            # Create a set with the section, values
            items = [
                (
                    section, Section(parser.items(section))
                )
            ]
            # Update the dictionary
            self.__dict__.update(items)