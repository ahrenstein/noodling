#!/usr/bin/env python3
"""Search the a Google Sheet pubhtml for pugs

"""
#
# Python Script:: pug_finder.py
#
# Linter:: pylint
#
# Copyright 2020, Matthew Ahrenstein, All Rights Reserved.
#
# Maintainers:
# - Matthew Ahrenstein: @ahrenstein
#
# See LICENSE
#

import argparse
import re
import sys
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests


# Email sending function
def send_email(email_address, ses_access_key, ses_secret_key, body):
    """A function to send email via AWS SES

    Args:
        email_address: An email address to send the results to
        ses_access_key: An AWS SES Access Key
        ses_secret_key: An AWS SES Secret Key
        body: The message body
    """
    # hard-coded variables
    sender_email = "pug-finder@route1337.com"
    sender_name = "Pug Finder"
    subject = "Pug Finder Results"

    # Begin code using example from
    # https://docs.aws.amazon.com/ses/latest/DeveloperGuide/examples-send-using-smtp.html #
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr((sender_name, sender_email))
    msg['To'] = email_address
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(body, 'plain')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    # Try to send the message.
    try:
        server = smtplib.SMTP("email-smtp.us-east-1.amazonaws.com", "587")
        server.ehlo()
        server.starttls()
        # stmplib docs recommend calling ehlo() before & after starttls()
        server.ehlo()
        server.login(ses_access_key, ses_secret_key)
        server.sendmail(sender_email, email_address, msg.as_string())
        server.close()
    # Display an error message if something goes wrong.
    except Exception as err:
        print("Error: ", err)
    else:
        print("Email sent!")
    # End example code #


# Main function
def main(email_address, ses_access_key, ses_secret_key, google_sheet):
    """The main function where we do all the work

    Args:
        email_address: An email address to send the results to
        ses_access_key: An AWS SES Access Key
        ses_secret_key: An AWS SES Secret Key
        google_sheet: A public Google Sheet's pubhtml URL
    """
    # Instantiate email_body string
    email_body = ""
    # Set the breed to search for
    search_breed = "PUG"
    # Get the contents of the page
    page = requests.get(google_sheet).text
    soup = BeautifulSoup(page, "lxml")
    # Search the rendered lowercase "soup" page for pugs
    search_results = soup.find_all(string=re.compile('.*{0}.*'
                                                     .format(search_breed)), recursive=True)
    print('Found the word "{0}" {1} times\n'.format(search_breed, len(search_results)))
    email_body = email_body + 'Found the word "{0}" {1} times\n'\
        .format(search_breed, len(search_results)) + "\n"
    # Send the email
    send_email(email_address, ses_access_key, ses_secret_key, email_body)
    sys.exit(0)


if __name__ == '__main__':
    # This function parses and return arguments passed in
    # Assign description to the help doc
    PARSER = argparse.ArgumentParser(
        description="Search a Google Sheet pubhtml for pugs")
    # Add arguments
    PARSER.add_argument(
        '-e', '--emailAddress', type=str, help='Email address to send results to', required=True)
    PARSER.add_argument(
        '-a', '--SESAccessKey', type=str, help='AWS SES Access Key', required=True)
    PARSER.add_argument(
        '-s', '--SESSecretKey', type=str, help='AWS SES Secret Key', required=True)
    PARSER.add_argument(
        '-g', '--GoogleSheet', type=str, help='A Google Sheet pubhtml page', required=True)
    # Array for all arguments passed to script
    ARGS = PARSER.parse_args()
    # Assign args to variables
    ARG_EMAIL = ARGS.emailAddress
    ARG_ACCESS_KEY = ARGS.SESAccessKey
    ARG_SECRET_KEY = ARGS.SESSecretKey
    ARG_GOOGLE_SHEET = ARGS.GoogleSheet
    main(ARG_EMAIL, ARG_ACCESS_KEY, ARG_SECRET_KEY, ARG_GOOGLE_SHEET)
