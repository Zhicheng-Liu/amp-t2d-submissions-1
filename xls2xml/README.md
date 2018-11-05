xls2xml module
==============

### What is This?
This simple tool suite is for validating xls, converting xls to tsv or xml file.

### Prerequisites
This package depends on the following packages (e.g. on RedHat 7):
```commandline
gcc openssl-devel bzip2-devel libxml2 libxml2-devel libxslt libxslt-devel python-wheel python2-pip
```
To install all the other Python dependencies with virtualenv:
```commandline
git clone https://github.com/EBIvariation/amp-t2d-submissions
cd amp-t2d-submissions/xls2xml
virtualenv -p python2.7 venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```
Making this tool portable (on similar system):
```commandline
# First copy all the files including virtualenv ENV to their new destination
# Then in the new location, replace the absolute paths in the script
sed -i 's/\/path\/to\/old\/venv/\/path\/to\/new\/venv/g' venv/bin/*
source venv/bin/activate
# Run your jobs
deactivate
```

### Using the scripts
There are a few scripts you can run under xls2xml subdirectory:
```commandline
validate_xls.py
validate_tsv.py
xls2tsv.py
xls2xml.py
tsv2xml.py
```
Before running these scripts, you'd better to activate virtualenv for correct environments:
```commandline
cd amp-t2d-submissions/xls2xml
source venv/bin/activate
```
Please refer to their command line help for information about what they do and which arguments are required. e.g.:
```commandline
python ./xls2xml/xls2xml.py -h
```
Here are some of the examples you could try out:
```commandline
python ./xls2xml/validate_xls.py --conf tests/data/T2D_xls2xml_v3.conf --schema tests/data/T2D_xls2xml_v1.schema tests/data/example_AMP_T2D_Submission_form_V2.xlsx 
python ./xls2xml/validate_tsv.py --conf tests/data/T2D_xls2xml_v3.conf --conf-key Sample --schema tests/data/T2D_xls2xml_v1.schema tests/data/example_samples.tsv
python ./xls2xml/xls2tsv.py --conf tests/data/T2D_xls2xml_v3.conf --conf-key Sample --schema tests/data/T2D_xls2xml_v1.schema tests/data/example_AMP_T2D_Submission_form_V2.xlsx tests/data/output_xls2tsv.tsv
python ./xls2xml/tsv2xml.py --conf tests/data/T2D_xls2xml_v3.conf --conf-key Sample --schema tests/data/T2D_xls2xml_v1.schema --xslt tests/data/T2D_xls2xml_v1.xslt tests/data/example_samples.tsv tests/data/output_tsv2xml.xml
python ./xls2xml/xls2xml.py --conf tests/data/T2D_xls2xml_v3.conf --conf-key Analysis --schema tests/data/T2D_xls2xml_v1.schema --xslt tests/data/T2D_xls2xml_v2.xslt tests/data/example_AMP_T2D_Submission_form_V2.xlsx tests/data/output_xls2xml_single.xml
python ./xls2xml/xls2xml.py --conf tests/data/T2D_xls2xml_v3.conf --conf-key Analysis,File --schema tests/data/T2D_xls2xml_v1.schema --xslt tests/data/T2D_xls2xml_v2.xslt tests/data/example_AMP_T2D_Submission_form_V2.xlsx tests/data/output_xls2xml_multiple.xml
python ./xls2xml/tsv2xml.py --conf tests/data/T2D_xls2xml_v3.conf --conf-key Analysis --schema tests/data/T2D_xls2xml_v1.schema --xslt tests/data/T2D_xls2xml_v2.xslt tests/data/example_analysis.tsv tests/data/output_tsv2xml_single.xml
python ./xls2xml/tsv2xml.py --conf tests/data/T2D_xls2xml_v3.conf --conf-key Analysis,File --schema tests/data/T2D_xls2xml_v1.schema --xslt tests/data/T2D_xls2xml_v2.xslt tests/data/example_analysis.tsv,tests/data/example_files.tsv tests/data/output_tsv2xml_multiple.xml
```

### Writing the configuration files
There are a few different configuration files for these scripts. The examples of each could be found in tests/data:
```commandline
tests/data/T2D_xls2xml_v3.conf
tests/data/T2D_xls2xml_v1.schema
tests/data/T2D_xls2xml_v2.xslt # for combining multiple worksheets into a single xml file
tests/data/T2D_xls2xml_v3.xslt # for allowing user defined columns
```

For the details of how they they should be written, there are comments in each examples above.

There are other data files served as test cases input. They are also used in the example usages as illustrated above:
```commandline
tests/data/example_AMP_T2D_Submission_form_V3.xlsx
tests/data/example_samples.tsv
tests/data/example_samples.xml
tests/data/example_analysis.xml
```
