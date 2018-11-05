import pytest
from StringIO import StringIO
from lxml import etree
from xls2xml import utils
from xls2xml import TSVReader
from xls2xml import XLSReader

def test_header_to_xml_tag():
    # are case-sensitive
    assert 'This_is_XML_tag' == utils.header_to_xml_tag('This_is_XML_tag')
    # cannot start with the letters xml (or XML, or Xml, etc)
    assert '__tag' == utils.header_to_xml_tag('XML_tag')
    assert '__tag' == utils.header_to_xml_tag('Xml_tag')
    assert '__tag' == utils.header_to_xml_tag('xml_tag')
    assert '_xml_tag' == utils.header_to_xml_tag('_xml_tag')
    # must start with a letter or underscore
    assert 'first_XML_tag' == utils.header_to_xml_tag('first_XML_tag')
    assert '_first_XML_tag' == utils.header_to_xml_tag('_first_XML_tag')
    assert '_st_XML_tag' == utils.header_to_xml_tag('1st_XML_tag')
    # contain only letters, digits, hyphens, underscores and periods
    assert 'this_one_XML_tag' == utils.header_to_xml_tag('this_one_XML_tag')
    assert 'this_1_XML_tag' == utils.header_to_xml_tag('this_1_XML_tag')
    assert 'this-one-XML-tag' == utils.header_to_xml_tag('this-one-XML-tag')
    assert 'this_1.0_XML_tag' == utils.header_to_xml_tag('this_1.0_XML_tag')
    assert 'this_____________________________XML_tag' == \
           utils.header_to_xml_tag('this_!@#$%^&*()+={}[]:;|\/?<>,~`_XML_tag')
    # cannot contain spaces
    assert '_this_XML_tag_' == utils.header_to_xml_tag(' this XML tag ')

def test_validate_file():
    validation_schema = 'data/T2D_xls2xml_v1.schema'
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Sample')
    assert utils.validate_file(tsv_reader, validation_schema)
    xls_reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    xls_reader.set_current_conf_key('Sample')
    assert utils.validate_file(xls_reader, validation_schema)

def test_extract_rows():
    validation_schema = 'data/T2D_xls2xml_v1.schema'

    rows = []
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Sample')
    assert utils.extract_rows(tsv_reader, 'Sample', validation_schema, rows)
    assert isinstance(rows, list)
    assert 6 == len(rows)
    tsv_reader = TSVReader('data/example_samples.tsv', 'data/T2D_xls2xml_v3.conf', 'Sample')
    for a, b in zip(rows, tsv_reader):
        assert 0 == cmp(a, b)

    rows = []
    xls_reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    assert utils.extract_rows(xls_reader, 'Sample', validation_schema, rows)
    assert isinstance(rows, list)
    assert 6 == len(rows)
    xls_reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    xls_reader.set_current_conf_key('Sample')
    for a, b in zip(rows, xls_reader):
        assert 0 == cmp(a, b)

    rows = []
    assert not utils.extract_rows(xls_reader, 'FalseExpected', validation_schema, rows)

def test_rows_to_xml():
    rows = []
    xls_reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    assert utils.extract_rows(xls_reader, 'Sample', 'data/T2D_xls2xml_v1.schema', rows)
    xml = utils.rows_to_xml(rows, 'Sample')
    assert isinstance(xml, etree._Element)
    assert xml.tag == 'SampleSet'
    assert len(rows) == len(xml)
    for row, child in zip(rows, xml):
        assert child.tag == 'Sample'
        assert {header : str(row.get(header, '')) for header in row} !=\
               {e.tag: e.text for e in child}
        assert {utils.header_to_xml_tag(header) : str('' if row.get(header, '') is None else row.get(header, ''))
                for header in row} == {e.tag : e.text for e in child}

def test_transform_xml():
    rows = []
    xls_reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    assert utils.extract_rows(xls_reader, 'Sample', 'data/T2D_xls2xml_v1.schema', rows)
    input_xml = utils.rows_to_xml(rows, 'Sample')
    output_xml = utils.transform_xml(input_xml, 'data/T2D_xls2xml_v3.xslt')
    with open('data/example_samples.xml') as example_xml:
        assert example_xml.readline() == "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        assert etree.tostring(output_xml, pretty_print=True) == example_xml.read()

def test_save_xml():
    rows = []
    xls_reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    assert utils.extract_rows(xls_reader, 'Sample', 'data/T2D_xls2xml_v1.schema', rows)
    input_xml = utils.rows_to_xml(rows, 'Sample')
    transformed_xml = utils.transform_xml(input_xml, 'data/T2D_xls2xml_v3.xslt')
    io_stream = StringIO()
    utils.save_xml(transformed_xml, io_stream)
    io_stream.seek(0)
    assert io_stream.read() == open('data/example_samples.xml').read()
    io_stream.close()

def test_write_empty_xml():
    rows = []
    xls_reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    assert utils.extract_rows(xls_reader, 'File', 'data/T2D_xls2xml_v1.schema', rows)
    input_xml = utils.rows_to_xml(rows, 'File')
    transformed_xml = utils.transform_xml(input_xml, 'data/T2D_xls2xml_v3.xslt')
    assert transformed_xml.getroot() is None # to make sure the transformed_xml is empty
    with open('data/out_empty.xml', 'w') as xml_file:
        utils.save_xml(transformed_xml, xml_file)

def test_multiple_sheets_to_xml():
    xls_reader = XLSReader('data/example_AMP_T2D_Submission_form_V3.xlsx', 'data/T2D_xls2xml_v3.conf')
    xls_readers = [ ('Analysis', xls_reader), ('File', xls_reader) ]
    output_xml = utils.multiple_objects_to_xml(xls_readers, 'data/T2D_xls2xml_v1.schema',
                                               'data/T2D_xls2xml_v2.xslt')
    with open('data/example_analysis.xml', 'r') as analysis_example:
        assert analysis_example.readline()
        assert etree.tostring(output_xml, pretty_print=True) == analysis_example.read()

    with pytest.raises(Exception):
        xls_readers = [ ('Exception', xls_reader), ('Expected', xls_reader) ]
        utils.multiple_objects_to_xml(xls_readers, 'data/T2D_xls2xml_v1.schema',
                                      'data/T2D_xls2xml_v2.xslt')

def test_multiple_tsvs_to_xml():
    analysis_tsv_reader = TSVReader('data/example_analysis.tsv', 'data/T2D_xls2xml_v3.conf', 'Analysis')
    files_tsv_reader = TSVReader('data/example_files.tsv', 'data/T2D_xls2xml_v3.conf', 'File')
    tsv_readers = [ ('Analysis', analysis_tsv_reader), ('File', files_tsv_reader) ]
    output_xml = utils.multiple_objects_to_xml(tsv_readers, 'data/T2D_xls2xml_v1.schema',
                                            'data/T2D_xls2xml_v2.xslt')
    with open('data/example_analysis.xml', 'r') as analysis_example:
        assert analysis_example.readline()
        assert etree.tostring(output_xml, pretty_print=True) == analysis_example.read()

    with pytest.raises(Exception):
        tsv_readers = [
            ('Exception', TSVReader('data/example_analysis.tsv', 'data/T2D_xls2xml_v3.conf', 'Exception')),
            ('Expected', TSVReader('data/example_analysis.tsv', 'data/T2D_xls2xml_v3.conf', 'Expected'))
        ]
        utils.multiple_objects_to_xml(tsv_readers, 'data/T2D_xls2xml_v1.schema',
                                      'data/T2D_xls2xml_v2.xslt')
