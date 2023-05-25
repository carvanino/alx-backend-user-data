#!/usr/bin/env python3
"""
Hold the function filter_datum which returns an obfuscated log message
"""


import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, separator: str) -> str:
    """
    Returns an obfuscated log message
    Args:
        fields: List - A list of strings representing the fields to obfuscate
        redaction: str - Representing what the field will be obfuscated by
        message: str - Representing the log line
        separator: str - Represent the character that separates all fields
                        in the log line
    """
    for field in fields:
        pattern = r'({}=)([^{}]+)'.format(field, separator)
        message = re.sub(pattern, r'\1{}'.format(redaction), message)
    return message
