"""Entrypoint to parse file
"""
from parser import MyParser
import os
import argparse
import config
import logging
import json

# use custom logger if available, otherwise basic one
if os.path.exists(config.LOGGER_PATH):
    with open(config.LOGGER_PATH, 'rt') as f:
        config_dict = json.load(f)
        logging.config.dictConfig(config_dict)
else:
    logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Get the desired option from user using an argument parser from command line
    # only spcs is required, delimiter and numlines ca be defined with default
    arg_parser = argparse.ArgumentParser()

    # enforce the user to use a specs file
    arg_parser.add_argument("-s", "--spec", required=True, help="Specs")

    # since delimiter is not in specs, let the user to pass it as an argument
    arg_parser.add_argument("-d", "--delimiter", required=False, help="Delimiter")

    # since delimiter is not in specs, let the user to pass it as an argument
    arg_parser.add_argument("-n", "--numlines", required=False, help="Number of lines in file")

    args = vars(arg_parser.parse_args())

    spec_filename = args["spec"]
    delimiter = args["delimiter"]
    
    if args["numlines"]:
        numlines = args["numlines"]
    
    if os.path.exists(spec_filename):
        myParser = MyParser(spec_filename)
        fixed_filename = myParser.generate_fixed_file()
        delimited_filename = myParser.generate_delimited_file(fixed_filename)
    else:
        logger.info("No valid specs file found (%s). Nothing to do! :(",spec_filename)