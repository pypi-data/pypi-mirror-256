"""
@author: Fernando Penaherrera @UOL/OFFIS

Utility functions for the MOSAIK PVLib Adapter
"""

import os
from os.path import join


def convert_german_date(date="30.12.2021"):
    """Converts the date from the German format to the standard format with dashes

    Args:
        date (str, optional): Date in the format DD.MM.YYYY. Defaults to "30.12.2021".

    Returns:
        str: Date in the format YYYY-MM-DD
    """
    return date[6:] + "-" + date[3:5] + "-" + date[0:2]


def normalize_product_names(name):
    """Normalize the names to exclude special characters
    Useful to look names from the PVLib and pass them into the dictionaries


    Args:
        name (str): Name of the inverter or the module

    Returns:
        str: Name with replaced characters
    """

    BAD_CHARS = ' -.()[]:+/",'
    GOOD_CHARS = "____________"

    mapping = str.maketrans(BAD_CHARS, GOOD_CHARS)
    norm_name = name.translate(mapping)
    return norm_name


if __name__ == "__main__":

    pass
