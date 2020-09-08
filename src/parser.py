"""Generates a fixed width file using the provided spec and parse to a delimited file
"""


import json
import os
import logging
from logging.config import fileConfig
import sys
import string
import random
import config

# use custom logger if available, otherwise basic one
if os.path.exists(config.LOGGER_PATH):
    with open(config.LOGGER_PATH, 'rt') as f:
        config_dict = json.load(f)
        logging.config.dictConfig(config_dict)
else:
    logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)

class MyParser():
    """Generates a fixed with file and parse it into a delimited file
    """
    specs={}

    def __init__(self, specs_file):
        self.specs=self.get_specs(specs_file)


    def get_specs(self,filename):
        """Parse specs to generate files based on the file specified

        Parameters
        ----------
        filename : str
            Path to specs file

        Returns
        -------
        dict
            A dictionary of specs, empty dictionary if dictionary not found or invalid
        """
        try:
            specs = {}
            if os.path.exists(filename):
                with open(filename) as specs_file:
                    specs = json.load(specs_file)
                    # Check if all keys are in the specs file, offsets are numeric and matches with columns
                    # TODO: Check keys one by one to specify more concise logging
                    if all (skey in specs for skey in ("ColumnNames","Offsets","FixedWidthEncoding","IncludeHeader","DelimitedEncoding")):
                        if not all(value.isdigit() for value in specs["Offsets"]):
                            logger.error("Invalid offset %s",all(value.isdigit() for value in specs["Offsets"]))
                            specs = {}
                        elif len(specs["Offsets"]) != len(specs["ColumnNames"]):
                            logger.error("Number of offsets and column names must be the same")
                            specs = {}
                            
                    else:
                        logger.error("At least one configuration was not found in the specs file")
                        specs = {}

        except Exception as e:
            logger.error("Error loading specs in %s: %s",filename,e)
        finally:
            if specs:
                logger.info("Specs file %s parsed successfully!",filename)

            return specs

    def generate_random_string(self,size,onechar=True):
        """Generates a random string to put on file based on ascii lowercase set

        Parameters
        ----------
        size : int
            Length of string
        onechar : bool, optional
            if true it will generates the same char as specified in size

        Returns
        -------
        str
            Random string generated
        """
        char_set = string.ascii_lowercase
        if onechar:
            generated = random.choice(char_set) * size
        else:
            generated = ''.join(random.choice(char_set) for ch in range(size))

        return generated

    def generate_fixed_file(self,numlines=config.DEFAULT_NUMLINES):
        """Deal exclusively with unicode objects as much as possible by decoding 
        things to unicode objects when you first get them and encoding them as necessary on the way out.

        Parameters
        ----------
        numlines : int
            Number of lines to be generated

        Returns
        -------
        generated file or None if an error ocurred
        """

        try:
            # if no specs available then we sholud not continue
            generated_file = None
            if not self.specs:
                raise Exception('Specs not found', 'Invalid specs')
            offsets = self.specs["Offsets"]

            # Create a format to generate the string. The string will be given by sequential order in offset specs
            format_line = "".join(["{:"+offset+"s}" for offset in offsets])

            # write in logs the system encofing for information
            logger.info("OS System encoding: %s",sys.getfilesystemencoding())
            
            with open(config.OUTPUT_PATH+config.FIXED_FILENAME, mode="w",encoding=self.specs["FixedWidthEncoding"]) as out:
                logger.info("Generating file: %s",config.OUTPUT_PATH+config.FIXED_FILENAME)
                # write the header first if necessary, other wise generate random strings to write them line by line
                # applies the format to the string generated to match with specs
                
                if self.specs["IncludeHeader"]:
                    columns = self.specs["ColumnNames"]
                    # TODO: what if column is greater than offset? Validate this in specs to declare invalid specs
                    header = format_line.format(*columns)
                    out.write(header)   
                    out.write(config.BREAKLINE)  

                for line in range(numlines):
                    values = [self.generate_random_string(int(offset)) for offset in offsets]
                    text_line = format_line.format(*values)
                    out.write(text_line)
                    out.write(config.BREAKLINE)

                generated_file = os.path.abspath(config.OUTPUT_PATH+config.FIXED_FILENAME)
                logger.info("Fixed-width file generated: %s",generated_file)
                        
        except Exception as e:
            logger.error(e)
            generated_file = None

        finally:
            return generated_file

    def generate_delimited_file(self,source_filename,separator=config.DEFAULT_DELIMITER):
        """Generates a file based on `source_filename` with the `separator` specified

        Parameters
        ----------
        source_filename : str
            Path to the file is needed to be parsed
        separator : str
            String to be used as delimiter
        """

        try:
            # if not specs found then no need to process
            generated_file = None
            if not self.specs:
                raise Exception('Specs not found', 'Invalid specs')

            columns = self.specs["ColumnNames"]
            offsets = self.specs["Offsets"]

            # create a format joined by separator
            format_line = separator.join(["{}" for column in columns])

            with open(config.OUTPUT_PATH+config.DELIMITED_FILENAME, mode="w",encoding=self.specs["DelimitedEncoding"]) as out:
                logger.info("Generating file: %s",config.OUTPUT_PATH+config.DELIMITED_FILENAME)
                if self.specs["IncludeHeader"]:
                    # TODO: what if column is greater than offset?
                    header = format_line.format(*columns)
                    out.write(header)   
                    out.write(config.BREAKLINE)
                # open the fixed width file
                with open(source_filename, mode="r",encoding=self.specs["FixedWidthEncoding"]) as inp:
                    logger.info("Parsing from: %s",source_filename)
                    # we will skip the first row if we need to include header and process the file line by line
                    if self.specs["IncludeHeader"]:
                        next(inp)

                    for line in inp:
                        init = 0
                        fields = []
                        # create a list of fields values to be formatted
                        for offset in offsets:
                            fields.append(line[init:init+int(offset)])
                            init += int(offset)

                        text_line = format_line.format(*fields)
                        out.write(text_line)
                        out.write(config.BREAKLINE)
                    
                    generated_file = os.path.abspath(config.OUTPUT_PATH+config.DELIMITED_FILENAME)
                    logger.info("Delimited file generated: %s",generated_file)
        except Exception as e:
            logger.error(e)
            generated_file = None
        finally:
            return generated_file
