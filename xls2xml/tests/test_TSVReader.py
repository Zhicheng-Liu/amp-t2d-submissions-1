from xls2xml import TSVReader

def test_get_valid_conf_keys():
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Sample')
    assert set(tsv_reader.get_valid_conf_keys()) == {'Sample'}
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Analysis')
    assert tsv_reader.get_valid_conf_keys() == []

def test_set_current_conf_key():
    # set_current_conf_key() should does nothing
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Sample')
    assert tsv_reader.is_valid()
    assert set(tsv_reader.get_valid_conf_keys()) == {'Sample'}
    tsv_reader.set_current_conf_key('Analysis')
    assert tsv_reader.is_valid()
    assert set(tsv_reader.get_valid_conf_keys()) == {'Sample'}
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Analysis')
    assert not tsv_reader.is_valid()
    assert tsv_reader.get_valid_conf_keys() == []
    tsv_reader.set_current_conf_key('Sample')
    assert not tsv_reader.is_valid()
    assert tsv_reader.get_valid_conf_keys() == []


def test_is_not_valid():
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Analysis')
    assert not tsv_reader.is_valid()

def test_is_valid():
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Sample')
    assert tsv_reader.is_valid()

def test_get_current_headers():
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Sample')
    headers = tsv_reader.get_current_headers()
    assert isinstance(headers, list)
    assert set(headers) == {'Sample_ID', 'Subject_ID', 'Geno_ID', 'Phenotype', 'Gender', 'Analysis_alias', 'Cohort ID',
                            'Ethnicity', 'Ethnicity Description', 'T2D', 'Case_Control', 'Description', 'Center_name',
                            'Hispanic or Latino; of Spanish origin', 'Age', 'Year of Birth', 'Year of first visit',
                            'Cell Type', 'Maternal_id', 'Paternal_id', 'Novel Attributes', 'Attribute_[test_column_2]',
                            'Attribute_[test_column_1]', 'Attribute_[add_value]'}

def test_next():
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Sample')
    row = tsv_reader.next()
    assert isinstance(row, dict)
    print(row)
    assert 0 == cmp(row, {'Hispanic or Latino; of Spanish origin': None, 'Phenotype': 'MeSH:D006262',
                          'Attribute_[test_column_1]': 'attribute_test_value_1_1', 'Description': 'Male normal',
                          'Center_name': 'WTGC cambridge', 'Case_Control': 'Control', 'T2D': 0,
                          'Analysis_alias': 'AN001', 'Geno_ID': None, 'Year of first visit': None, 'Cell Type': 'Blood',
                          'Maternal_id': 'SAM111113', 'Gender': 'male', 'Subject_ID': 'SAM111111',
                          'Paternal_id': 'SAM111115', 'Cohort ID': 'CO1111',
                          'Attribute_[test_column_2]': 'attribute_test_value_2_1', 'Novel Attributes': None,
                          'Ethnicity Description': None, 'Year of Birth': '1986', 'Sample_ID': 'SAM111111', 'Age': '31',
                          'Ethnicity': 'EUWH'})
    for row in tsv_reader:
        assert isinstance(row, dict)
