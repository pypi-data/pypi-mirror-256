#!/usr/bin/env python3
from nsrx_class import cli_loop
from nsrx_class.logger_config import setup_logging
import logging

# Call the setup_logging function from logger_config
setup_logging()

module_name = __name__.split('.')[-1]


def main():

    logging.debug(f' {module_name} This is a debug message in some_module')
    logging.info(f' {module_name} This is an info message in some_module')


    cli_loop.main_cli_loop()
    

    

if __name__ == "__main__":
    main()

