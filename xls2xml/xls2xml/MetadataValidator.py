"""
This module validate data with a given schema

This module depends on cerberus and pyyaml
"""

from __future__ import print_function
import sys
import yaml
from CustomValidator import CustomValidator

class MetadataValidator(object):
    """
    Data validation with a given schema
    """

    def __init__(self, schema_filename):
        """
        Constructor

        :param schema_filename: schema definition file path
        :type schema_filename: basestring
        """
        with open(schema_filename, 'r') as schema_file:
            schema = yaml.load(schema_file)
            self.validator = CustomValidator(schema=schema)
            self.validator.allow_unknown = True

    def validate_data(self, data, schema_key):
        """
        Validate a data set

        :param data: the actual data
        :type data: dict
        :param schema_key: key to access the definition in the schema file
        :type schema_key: basestring
        :return: True if the data passes the validation
        :rtype: bool
        """
        document = {}
        document[schema_key] = data
        if not self.validator.validate(document=document):
            print(self.validator.errors, file=sys.stderr)
            return False

        return True

    def get_errors(self):
        """
        Getter for the validation errors

        :return: validation error for last validation call
        :rtype: basestring
        """
        return self.validator.errors
