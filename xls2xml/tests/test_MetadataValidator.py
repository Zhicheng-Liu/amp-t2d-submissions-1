from xls2xml import MetadataValidator
from xls2xml import XLSReader
from xls2xml import TSVReader

def test_valid_data():
    validator = MetadataValidator('data/T2D_xls2xml_v1.schema')
    reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    reader.active_worksheet = 'Sample'
    row = reader.next()
    assert validator.validate_data(row, 'Sample')
    reader.active_worksheet = 'Analysis'
    row = reader.next()
    assert validator.validate_data(row, 'Analysis')
    reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Sample')
    row = reader.next()
    assert validator.validate_data(row, 'Sample')

def test_invalid_data():
    validator = MetadataValidator('data/T2D_xls2xml_v1.schema')
    reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    reader.active_worksheet = 'Sample'
    row = reader.next()
    assert not validator.validate_data(row, 'Analysis')
    reader.active_worksheet = 'Analysis'
    row = reader.next()
    assert not validator.validate_data(row, 'Sample')
    reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Sample')
    row = reader.next()
    assert not validator.validate_data(row, 'Analysis')
