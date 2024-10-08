#!/usr/bin/env python3
"""Some crypto functions for use in various scripts"""
#
# Python Script:: crypto_functions.py
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

import base64
import datetime
import json
import time
import hmac
import hashlib
import requests
from requests.auth import AuthBase


# List of tokens to use the Coinbase API for instead of CoinMarketCap
COINBASE_TOKENS = ["BTC", "AERO", "ALGO", "DOGE", "XRP", "ADA", "ETH", "POL", "ALCX", "ENS"]
# List of tokens that can't currently be tracked
UNTRACKED_TOKENS = ["robot", "citadao"]


# Create custom authentication for CoinbasePro
# as per https://docs.pro.coinbase.com/?python#creating-a-request
class CoinbaseProAuth(AuthBase):
    """
        Coinbase Pro provided authentication method with minor fixes
        """
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


# Create custom authentication for Coinbase API
# as per https://developers.coinbase.com/docs/wallet/api-key-authentication
class CoinbaseWalletAuth(AuthBase):
    """
    Coinbase provided authentication method with minor fixes
    """
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def __call__(self, request):
        timestamp = str(int(time.time()))
        message = timestamp + request.method + request.path_url + (request.body or '')
        # Coinbase's code example is wrong. The key and message must be converted to bytes for HMAC
        key_bytes = bytes(self.secret_key, 'latin-1')
        data_bytes = bytes(message, 'latin-1')
        signature = hmac.new(key_bytes, data_bytes, hashlib.sha256).hexdigest()

        request.headers.update({
            'CB-ACCESS-SIGN': signature,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
        })
        return request


def get_coinbase_creds_from_file(credentials_file):
    """Open a JSON file and get Coinbase credentials out of it
    Args:
        credentials_file: A JSON file containing Coinbase credentials

    Returns:
        coinbase_api_key: An API key for Coinbase APIv2
        coinbase_api_secret: An API secret for Coinbase APIv2
    """
    with open(credentials_file) as creds_file:
        data = json.load(creds_file)
    coinbase_api_key = data['API_Key']
    coinbase_api_secret = data['API_Secret']
    return coinbase_api_key, coinbase_api_secret


def get_cbpro_creds_from_file(credentials_file):
    """Open a JSON file and get Coinbase Pro credentials out of it
    Args:
        credentials_file: A JSON file containing Coinbase Pro credentials

    Returns:
        cbpro_api_key: An API key for Coinbase Pro
        cbpro_api_secret: An API secret for Coinbase Pro
        cbpro_api_passphrase: An API passphrase for Coinbase Pro
    """
    with open(credentials_file) as creds_file:
        data = json.load(creds_file)
    cbpro_api_key = data['API_Key']
    cbpro_api_secret = data['API_Secret']
    cbpro_api_passphrase = data['Passphrase']
    return cbpro_api_key, cbpro_api_secret, cbpro_api_passphrase


def coinmarketcap_price_check(cmc_api_key, coin):
    """Check the price of a cryptocurrency against CoinMarketCap to see
    if it fell below the minimum price
    Args:
        cmc_api_key: The CoinMarketCap API key
        coin: The coin/token that we care about
    Returns:
        coin_current_price: The current price of the coin
    """
    request_url = (f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/"
                   f"latest?slug={coin}&convert=USD")
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": cmc_api_key,
    }

    response = requests.get(request_url, headers=headers, timeout=60)
    data = response.json()
    for key in data["data"]:
        coin_current_price = data["data"][key]["quote"]["USD"]["price"]
    return coin_current_price


def coinbase_price_check(coinbase_api_key, coinbase_api_secret,
                         coin):
    """Check the price of a cryptocurrency against Coinbase to see
    if it fell below the minimum price
    Args:
        coinbase_api_key: An API key for Coinbase APIv2
        coinbase_api_secret: An API secret for Coinbase APIv2
        coin: The coin/token that we care about
    Returns:
        coin_current_price: The current price of the coin
    """
    # Instantiate Coinbase API and query the price
    api_url = 'https://api.coinbase.com/v2/'
    coinbase_auth = CoinbaseWalletAuth(coinbase_api_key, coinbase_api_secret)
    api_query = "prices/%s-USD/spot" % coin
    result = requests.get(api_url + api_query, auth=coinbase_auth, timeout=60)
    coin_current_price = float(result.json()['data']['amount'])
    return coin_current_price


def cbpro_tx_grab(cbpro_api_key, cbpro_api_secret, cbpro_api_passphrase, hours):
    """Grab all Coinbase Pro transactions in the last X hours
    Args:
        cbpro_api_key: An API key for Coinbase Pro
        cbpro_api_secret: An API secret for Coinbase Pro
        cbpro_api_passphrase: An API passphrase for Coinbase Pro
        hours: How far back in hours you want to look

    Returns:
        result: Coinbase transactions as request Response
    """
    # Instantiate Coinbase API and query the price
    timestamp = (datetime.datetime.utcnow() - datetime.timedelta(hours=hours)).isoformat()
    api_url = 'https://api.pro.coinbase.com/'
    coinbase_auth = CoinbaseProAuth(cbpro_api_key, cbpro_api_secret, cbpro_api_passphrase)
    api_query = "transfers?before=%s" % timestamp
    result = requests.get(api_url + api_query, auth=coinbase_auth, timeout=60)
    return result


def cbpro_order_grab(cbpro_api_key, cbpro_api_secret, cbpro_api_passphrase, hours):
    """Grab all Coinbase Pro Orders in the last X hours
    Args:
        cbpro_api_key: An API key for Coinbase Pro
        cbpro_api_secret: An API secret for Coinbase Pro
        cbpro_api_passphrase: An API passphrase for Coinbase Pro
        hours: How far back in hours you want to look

    Returns:
        result: Coinbase orders as request Response
    """
    # Instantiate Coinbase API and query the price
    timestamp = (datetime.datetime.utcnow() - datetime.timedelta(hours=hours)).isoformat()
    api_url = 'https://api.pro.coinbase.com/'
    coinbase_auth = CoinbaseProAuth(cbpro_api_key, cbpro_api_secret, cbpro_api_passphrase)
    api_query = 'orders?status=done&before=%s' % timestamp
    result = requests.get(api_url + api_query, auth=coinbase_auth, timeout=60)
    return result
