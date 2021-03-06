#!/usr/bin/env python3
"""A fast way to list all Coinbase Pro transactions for the last 12 hours"""
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
import requests
import crypto_functions


def main(coinbase_creds_file):
    """
    The main function where all code is called from

    Args:
    sheet_id: The UID of the Google Sheet
    credentials_file: The path to your Google credentials.json
    coinbase_creds_file: The path to your Coinbase coinbase_pro.json file
    """
    cbpro_creds = crypto_functions.get_cbpro_creds_from_file(coinbase_creds_file)
    result = crypto_functions.cbpro_tx_grab(cbpro_creds[0], cbpro_creds[1], cbpro_creds[2])
    transactions = result.json()
    print(json.dumps(transactions, indent=2))


if __name__ == '__main__':
    # This function parses and return arguments passed in
    # Assign description to the help doc
    PARSER = argparse.ArgumentParser(
        description='A fast way to list all Coinbase Pro'
                    ' transactions for the last 12 hours.')
    # Add arguments
    PARSER.add_argument(
        '-c', '--coinbaseCredsFile', type=str,
        help="The path to your Coinbase coinbase_pro.json file", required=True
    )
    # Array for all arguments passed to script
    ARGS = PARSER.parse_args()
    # Assign args to variables
    ARG_COINBASE_CREDS = ARGS.coinbaseCredsFile
    main(ARG_COINBASE_CREDS)
