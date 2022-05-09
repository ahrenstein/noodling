#!/usr/bin/env python3
"""Convert a DNS filter list to a Terraform variable"""
#
# Python Script:: dns_to_terraform.py
#
# Linter:: pylint
#
# Copyright 2022, Matthew Ahrenstein, All Rights Reserved.
#
# Maintainers:
# - Matthew Ahrenstein: matt@ahrenstein.com
#
# See LICENSE
#

import logging
import re
import argparse
import requests


def is_line_domain(line_to_test: str) -> bool:
    """
   Check if a string is a valid domain

   Args:
   line_to_test: The string to test
   """
    # RegEx for a valid domain
    valid_domain_regex = re.compile("^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6}")
    # Check if the line is a valid domain and return results
    if re.search(valid_domain_regex, line_to_test):
        return True
    return False


def save_lists_to_terraform(terraform_file: str,
                            filtered_domains: list, filter_exceptions: list) -> None:
    """
   Convert domain lists in to terraform variables and saves them to a tf file

   Args:
   terraform_file: The path to save your Terraform file to
   filtered_domains: The list of domains to add to the filter variable
   filter_exceptions: The list of domains to add to the exceptions variable
   """
    with open(terraform_file, 'w') as tf_output:
        # Write the header of the file
        tf_output.write('# Auto-generated file from converting a DNS filter list\n\n\n')
        # Write the filter variable
        tf_output.write('#Filter list\nvariable "filter_list"'
                        ' {\n  description = "ADD_A_DESCERIPTION"\n'
                        '  type = list(string)\n  default = [\n')
        for entry in filtered_domains:
            tf_output.write(f"  \"{entry}\",\n")
        tf_output.write('  ]\n}\n\n')
        if filter_exceptions:
            # Write the exception variable
            tf_output.write('#Exception list\nvariable "exception_list"'
                            ' {\n  description = "ADD_A_DESCERIPTION"\n'
                            '  type = list(string)\n  default = [\n')
            for entry in filter_exceptions:
                tf_output.write(f"  \"{entry}\",\n")
            tf_output.write('  ]\n}\n\n')
        tf_output.close()


def parse_filter_list(filter_file: str) -> [list, list]:
    """
    Open a local filter file and parse it

    Args:
    filter_file: The path to your filter file

    Returns:
    list_of_domains: The list of domains to filter
    list_of_exceptions: THe list of domains to make exceptions for
    """
    list_of_domains = []
    list_of_exceptions = []
    # Determine if the filter file is local or remote
    if filter_file.lower().startswith('http'):
        logging.info("The filter is a remote file")
        remote_source = requests.get(filter_file)
        with open("/tmp/filter.txt", 'wb') as remote_file:
            remote_file.write(remote_source.content)
            remote_file.close()
        loaded_file = "/tmp/filter.txt"
    else:
        loaded_file = filter_file
    # Parse the filter file
    with open(loaded_file) as file:
        lines = file.readlines()
        for line in lines:
            # If the line starts with "||" then it is an AdGuard rule
            if line.startswith("||"):
                # Strip out the characters found in a typical
                # AdGuard rule along with any newline characters
                domain = (re.sub('[|^]', '', line.strip()))
                if "*" in domain:
                    logging.warning("Unable to save %s due to a wildcard in the rule", domain)
                else:
                    logging.info("Saving %s to list of domains to filter", domain)
                    list_of_domains.append(domain)
            elif line.startswith("@@||"):
                # Save this domain to an exceptions list
                domain = (re.sub('[|@^]', '', line.strip()))
                if "*" in domain:
                    logging.warning("Unable to save %s due to a wildcard in the rule", domain)
                else:
                    logging.info("Saving %s to list of exception domains", domain)
            elif is_line_domain(line.strip()):
                domain = line.strip()
                logging.info("Saving %s to list of domains to filter", domain)
                list_of_domains.append(domain)
            elif line.startswith("127.0.0.1") or line.startswith("0.0.0.0"):
                domain = line.replace('127.0.0.1 ', '').replace('0.0.0.0 ', '').strip()
                logging.info("Saving %s to list of domains to filter", domain)
                list_of_domains.append(domain)
    return sorted(list_of_domains), sorted(list_of_exceptions)


def main(filter_file: str, terraform_file: str):
    """
    The main function where all code is called from

    Args:
    filter_file: The path to your filter file
    terraform_file: The path you want to output your Terraform code to
    """
    # Configure logging
    logging.basicConfig(level=logging.WARNING,
                        datefmt='%m/%d/%G %H:%M:%S', format='%(asctime)s %(message)s')
    list_of_domains = parse_filter_list(filter_file)[0]
    list_of_exceptions = parse_filter_list(filter_file)[1]
    save_lists_to_terraform(terraform_file, list_of_domains, list_of_exceptions)


if __name__ == '__main__':
    # This function parses and return arguments passed in
    # Assign description to the help doc
    PARSER = argparse.ArgumentParser(
        description='Convert a DNS filter list to a Terraform variable.')
    # Add arguments
    PARSER.add_argument(
        '-a', '--filterList', type=str,
        help="The path to your filter file", required=True
    )
    PARSER.add_argument(
        '-t', '--terraformFile', type=str, default="./list.tf",
        help="The path you want to output to", required=False
    )
    # Array for all arguments passed to script
    ARGS = PARSER.parse_args()
    # Assign args to variables
    ARG_FILTER_FILE = ARGS.filterList
    ARG_TF_FILE = ARGS.terraformFile
    main(ARG_FILTER_FILE, ARG_TF_FILE)
