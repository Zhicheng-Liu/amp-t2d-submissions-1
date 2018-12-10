import pytest
from xls2xml import XLSReader

def test_valid_worksheets():
    xls_reader =  XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    worksheets = xls_reader.valid_worksheets()
    assert isinstance(worksheets, list)
    assert set(worksheets) == {'Sample', 'Analysis', 'File'}

def test_get_valid_conf_keys():
    xls_reader =  XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    worksheets = xls_reader.valid_worksheets()
    assert isinstance(worksheets, list)
    assert set(worksheets) == {'Sample', 'Analysis', 'File'}

def test_set_current_conf_key():
    xls_reader =  XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    active_worksheet = xls_reader.active_worksheet
    assert active_worksheet is None
    xls_reader.set_current_conf_key('Sample')
    active_worksheet = xls_reader.active_worksheet
    assert active_worksheet == 'Sample'
    xls_reader.set_current_conf_key('Analysis')
    active_worksheet = xls_reader.active_worksheet
    assert active_worksheet == 'Analysis'

def test_get_current_headers():
    xls_reader =  XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    xls_reader.set_current_conf_key('Sample')
    headers = xls_reader.get_current_headers()
    assert isinstance(headers, list)
    assert set(headers) == {u'Sample_ID', u'Subject_ID', u'Geno_ID', u'Phenotype', u'Gender',
                            u'Analysis_alias', u'Cohort ID', u'Ethnicity', u'Ethnicity Description',
                            u'T2D', u'Case_Control', u'Description', u'Center_name',
                            u'Hispanic or Latino; of Spanish origin', u'Age', u'Year of Birth',
                            u'Year of first visit', u'Cell Type', u'Maternal_id', u'Paternal_id',
                            u'Novel Attributes',u'attribute_[test_column_2]',u'attribute_[test_column_1]',
                            u'attribute_[add_value]'}
    xls_reader.set_current_conf_key('Analysis')
    headers = xls_reader.get_current_headers()
    assert isinstance(headers, list)
    assert set(headers) == {u'Analysis_name', u'Analysis_alias', u'Title', u'Description',
                            u'Project_name', u'Experiment_type', u'Platform',
                            u'Standard_refname or Sequence_accession', u'Imputation',
                            u'Sequence_accession_label', u'External_link', u'Software',
                            u'Pipeline Description', u'Run Accession(s)', u'Center_name',
                            u'Analysis_date'}
    xls_reader.set_current_conf_key('ExceptionExpected')
    with pytest.raises(Exception):
        xls_reader.get_current_headers()

def test_next_row():
    xls_reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')

    xls_reader.set_current_conf_key('Sample')
    row = xls_reader.next()
    assert isinstance(row, dict)
    assert 0 == cmp(row, {'Hispanic or Latino; of Spanish origin': None, 'Phenotype': 'MeSH:D006262',
                          'attribute_[test_column_1]': 'attribute_test_value_1_1', 'row_num': 2,
                          'Description': 'Male normal', 'Center_name': 'WTGC cambridge', 'Case_Control': 'Control',
                          'T2D': 0L, 'Analysis_alias': 'AN001', 'Geno_ID': None, 'Year of first visit': None,
                          'Cell Type': 'Blood', 'Maternal_id': 'SAM111113', 'Gender': 'male', 'Subject_ID': 'SAM111111',
                          'Paternal_id': 'SAM111115', 'Cohort ID': 'CO1111',
                          'attribute_[test_column_2]': 'attribute_test_value_2_1', 'Novel Attributes': None,
                          'Ethnicity Description': None, 'Year of Birth': 1986L, 'Sample_ID': 'SAM111111', 'Age': 31L,
                          'Ethnicity': 'EUWH'})

    xls_reader.set_current_conf_key('Analysis')
    row = xls_reader.next()
    assert isinstance(row, dict)
    assert 0 == cmp(row, {'Pipeline Description': 'Alignment using BWA. Variant calling using the standard GATK pipeline. Association done using PLINK',
                          'Analysis_name': 'raremetalworker', 'Center_name': 'WTGC',
                          'Project_name': 'AMP DCC T2D  submission example', 'Description': None,
                          'Title': 'WTGC T2D Analysis', 'Standard_refname or Sequence_accession': 'GRCh37',
                          'Analysis_date': '2013-11-01T10:10:10.0Z', 'row_num': 2, 'Imputation': 0L,
                          'Platform': 'Illumina Genome Analyzer II', 'Experiment_type': 'Exome sequencing',
                          'Analysis_alias': 'AN001', 'Sequence_accession_label': None,
                          'Software': 'BWA, GATK, PLINK', 'Run Accession(s)': 'EGAR01000000002',
                          'External_link': None})
