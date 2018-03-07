"""
This module adds customised validation rules to the cerberus.Validator
"""
import urllib2
from cerberus import Validator

class CustomValidator(Validator):
    """
    Custom built validator
    """
    def _validate_PhenotypeOntology(self, isPhenotypeOntology, field, value):
        """
        Validate phenotype ontologies

        :param isPhenotypeOntology: whether the value is a valid phenotype term
        :type isPhenotypeOntology: bool
        :param field: the field name for the phenotype
        :type field: basestring
        :param value: the value of the field
        :type value: basestring
        :return: none
        :rtype:
        """
        db_ids = value.split(',')
        for db_id in db_ids:
            (db, id) = db_id.split(':')
            if db == 'MeSH': # Fetch information from MeSH API
                url = "https://id.nlm.nih.gov/mesh/" + id + ".json"
                json = urllib2.urlopen(url).read()
                if '@id' not in json:
                    self._error(field, "Must be a valid MeSH ID: " + db_id + "!")
            elif db == 'EFO': # Fetch information from Ensembl REST
                url = "https://rest.ensembl.org/ontology/id/" + db_id\
                      + "?content-type=application/json"
                try:
                    json = urllib2.urlopen(url).read()
                except urllib2.HTTPError as e:
                    self._error(field, "Must be a valid EFO ID: " + db_id + "!")
            else: # For anything else, treat them invalid
                self._error(field, 'Phenotype not recognised: ' + db_id)
