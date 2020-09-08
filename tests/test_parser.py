import pytest
import parser
from parser import MyParser
import os
import config
import csv

FIXED_FILENAME      =   "output/1.txt"
DELIMITED_FILENAME  =   "output/2.csv"


# TODO: Use fixture to create one instance of MyParser
def test_no_spec():
    """Tests no specs file avilable
    """
    filename = "nospec.json"
    myParser = MyParser(filename)
    assert not myParser.specs

def test_invalid_spec():
    """Tests an invalid specs. E.g. non numeric offsets or different number of columns and offsets
    """
    filename = "invalid_spec.json"
    myParser = MyParser(filename)
    assert not myParser.specs

def test_fixed_file_exists():
    """Tests a fixed file was generated
    """
    myParser = MyParser(config.SPEC_FILE)
    filename = myParser.generate_fixed_file()
    assert os.path.exists(filename)

def test_delimited_file_exists():
    """Tests a delimited file was generated
    """
    myParser = MyParser(config.SPEC_FILE)
    myParser.generate_delimited_file(source_filename=config.OUTPUT_PATH+config.FIXED_FILENAME)
    assert os.path.exists(config.OUTPUT_PATH+config.DELIMITED_FILENAME)

def test_fixed_file_is_valid():
    """Tests a fixed file is valid comparing the total width with expected
    """
    myParser = MyParser(config.SPEC_FILE)
    myParser.generate_fixed_file()
    total_offset = sum([int(off) for off in myParser.specs["Offsets"]])
    assert os.path.exists(config.OUTPUT_PATH+config.FIXED_FILENAME)

    if os.path.exists(config.OUTPUT_PATH+config.FIXED_FILENAME):
        with open(config.OUTPUT_PATH+config.FIXED_FILENAME, mode="r",encoding=myParser.specs["FixedWidthEncoding"]) as inp:
            for line in inp:
                assert len(line.replace(config.BREAKLINE, ""))==total_offset

def test_delimited_file_is_valid():
    """Tests a delimited file is valid comparing number of columns in every line with expeced
    """
    myParser = MyParser(config.SPEC_FILE)
    myParser.generate_delimited_file(source_filename=config.OUTPUT_PATH+config.FIXED_FILENAME)
    total_columns = len(myParser.specs["ColumnNames"])
    assert os.path.exists(config.OUTPUT_PATH+config.DELIMITED_FILENAME)

    if os.path.exists(config.OUTPUT_PATH+config.DELIMITED_FILENAME):
        with open(config.OUTPUT_PATH+config.DELIMITED_FILENAME, mode="r",encoding=myParser.specs["FixedWidthEncoding"]) as inp:
            delimited_reader = csv.reader(inp, delimiter=config.DEFAULT_DELIMITER, skipinitialspace=True)
            for line in delimited_reader:
                assert len(line)==total_columns

# TODO: Test encodings