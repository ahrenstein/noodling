#!/usr/bin/env python3
"""A fast way to list all Coinbase Pro transactions for the last X hours"""
#
# Python Script:: list_coinbase_pro_txs.py
#
# Linter:: pylint
#
# Copyright 2021, Matthew Ahrenstein, All Rights Reserved.
#
# Maintainers:
# - Matthew Ahrenstein: matt@ahrenstein.com
#
# See LICENSE
#

import argparse
import json
import crypto_functions


def main(coinbase_creds_file, hours):
    """
    The main function where all code is called from

    Args:
    coinbase_creds_file: The path to your Coinbase coinbase_pro.json file
    hours: How far back in hours you want to look
    """
    cbpro_creds = crypto_functions.get_cbpro_creds_from_file(coinbase_creds_file)
    # Get transactions for printing
    result = crypto_functions.cbpro_tx_grab(cbpro_creds[0], cbpro_creds[1], cbpro_creds[2], hours)
    transactions = json.dumps(result.json(), indent=2)
    if transactions == "[]":
        print("No transactions found in the last %s hours" % hours)
    else:
        print("Transactions in the last %s hours" % hours)
        print(transactions)


if __name__ == '__main__':
    # This function parses and return arguments passed in
    # Assign description to the help doc
    PARSER = argparse.ArgumentParser(
        description='A fast way to list all Coinbase Pro'
                    ' transactions for the last X hours.')
    # Add arguments
    PARSER.add_argument(
        '-c', '--coinbaseCredsFile', type=str,
        help="The path to your Coinbase coinbase_pro.json file", required=True
    )
    PARSER.add_argument(
        '-hr', '--hours', type=int,
        help="How many hours back do you want to look?", required=True
    )
    # Array for all arguments passed to script
    ARGS = PARSER.parse_args()
    # Assign args to variables
    ARG_COINBASE_CREDS = ARGS.coinbaseCredsFile
    ARG_HOURS = ARGS.hours
    main(ARG_COINBASE_CREDS, ARG_HOURS)
