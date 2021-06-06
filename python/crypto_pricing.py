#!/usr/bin/env python3
"""A fast way to grab the current value of various crypto currencies and
 update a private Google Sheet I have."""
#
# Python Script:: crypto_pricing.py
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
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import crypto_functions


def update_sheet_column(google_sheet, sheet_id, sheet_range, content):
    """
    Update a Google Sheet column range with a list of items

    Args:
    google_sheet: A Google service.spreadsheet object
    sheet_id: The unique ID of the Google Sheet
    sheet_range: The range of content in the Sheet!A1:B2 format
    content: A Python list of values
    """
    send_body = {
        "range": sheet_range,
        "majorDimension": "ROWS",
        "values": content
    }
    _ = google_sheet.values().update(spreadsheetId=sheet_id,
                                     range=sheet_range, valueInputOption='USER_ENTERED',
                                     body=send_body).execute()


def main(sheet_id, credentials_file, coinbase_creds_file):
    """
    The main function where all code is called from

    Args:
    sheet_id: The UID of the Google Sheet
    credentials_file: The path to your Google credentials.json
    coinbase_creds_file: The path to your Coinbase coinbase.json
    """
    # NOTE: All ranges are hardcoded as this script is for a very specific use case
    # Auth to Coinbase
    coinbase_creds = crypto_functions.get_coinbase_creds_from_file(coinbase_creds_file)
    # Auth to Google using https://developers.google.com/sheets/api/quickstart/python
    google_creds = None
    # The file token.pickle stores the user's access token, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            google_creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not google_creds or not google_creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_file, "https://www.googleapis.com/auth/spreadsheets")
        google_creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(google_creds, token)

    service = build('sheets', 'v4', credentials=google_creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range="Simple!H11:H52").execute()
    values = result.get('values', [])
    current_prices = []
    date_range = []
    if not values:
        print('No data found.')
    else:
        for row in values:
            # Hardcoding BANK to always be zero unless it starts seeing solid liquidity
            if row[0] in ["bankless-dao"]:
                current_prices.append([0])
            # Hardcoding QuickSwap liquidity tokens to $1 until I figure out a better method
            elif row[0].startswith("QUICK"):
                current_prices.append([1])
            # Logic to use CoinGecko for coins Coinbase doesn't like
            elif row[0] in ["defipulse-index", "dogecoin", "sushi",
                            "tribe-2", "ripple", "money-party",
                            "btc-2x-flexible-leverage-index"]:
                current_prices.append([crypto_functions.coingecko_price_check(row[0])])
            else:
                current_prices.append([crypto_functions.coinbase_price_check(
                    coinbase_creds[0], coinbase_creds[1], row[0])])
            date_range.append([datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")])
        update_sheet_column(sheet, sheet_id, "Simple!J11:J52", current_prices)
        update_sheet_column(sheet, sheet_id, "Simple!L11:L52", date_range)


if __name__ == '__main__':
    # This function parses and return arguments passed in
    # Assign description to the help doc
    PARSER = argparse.ArgumentParser(
        description='A fast way to grab the current value of various crypto'
                    ' currencies and update a private Google Sheet I have.')
    # Add arguments
    PARSER.add_argument(
        '-g', '--googleCredsFile', type=str,
        help="The path to your Google credentials.json", required=True
    )
    PARSER.add_argument(
        '-c', '--coinbaseCredsFile', type=str,
        help="The path to your Coinbase coinbase.json file", required=True
    )
    PARSER.add_argument(
        '-s', '--sheetID', type=str,
        help="The Google Sheet UID", required=True
    )
    # Array for all arguments passed to script
    ARGS = PARSER.parse_args()
    # Assign args to variables
    ARG_SHEET_ID = ARGS.sheetID
    ARG_GOOGLE_CREDS = ARGS.googleCredsFile
    ARG_COINBASE_CREDS = ARGS.coinbaseCredsFile
    main(ARG_SHEET_ID, ARG_GOOGLE_CREDS, ARG_COINBASE_CREDS)
