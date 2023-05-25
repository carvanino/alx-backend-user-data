#!/usr/bin/env python3
"""
Hold the function filter_datum which returns an obfuscated log message
"""


import re
from typing import List
import logging
import os
from mysql.connector import connection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
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
        # pattern = r'({}=)([^;]+|\w+)'.format(field)
        # pattern = r'({}=)(\d+.\d+.\d+|\w+)'.format(field)
        message = re.sub(pattern, r'\1{}'.format(redaction), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        # super().__init__(self.FORMAT)
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in Incoming log records using filter_datum """
        record.msg = filter_datum(
            self.fields, self.REDACTION,
            record.getMessage(), self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    Creates a logger user_data
    """
    user_data = logging.getLogger(__name__)
    user_data.setLevel(logging.INFO)
    # propagate determines if handlers of higher severity are ignored or not
    user_data.propagate = False
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    user_data.addHandler(stream_handler)
    return user_data


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to a database
    """
    USER = os.getenv('PERSONAL_DATA_DB_USERNAME') or 'root'
    PASSWORD = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ''
    HOST = os.getenv('PERSONAL_DATA_DB_HOST') or 'localhost'
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    cnx = connection.MySQLConnection(user=USER, password=PASSWORD,
                                     host=HOST, database=db)
    return cnx


def main():
    """
    Retrieves all rows from the users table and formats the PII
    """
    db = get_db()
    cursor = db.cursor()
    query = ('SELECT * FROM users')
    formatter = RedactingFormatter(list(PII_FIELDS))
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]
    for row in cursor:
        rec = dict(zip(columns, row))
        rec_msg = "; ".join("{}={}".format(key, repr(value))
                           for key, value in rec.items())
        record = logging.LogRecord(
            "user_data", logging.INFO, None, None, rec_msg, None, None
        )
        print(formatter.format(record))
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
