#!/usr/bin/env python3
"""Unwatch all repos in a GitHub org

"""
#
# Python Script:: unfollow_github_org.py
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
from github import Github


def main(github_token, github_org):
    """The main function where we do all the work

    Args:
        github_token: A GitHub PAT with access to your org
        github_org: The GitHub organization name that you want to unwatch repos for

    """
    # Instantiate all_repos value for return
    all_repos = []
    # Instantiate GitHub access
    gh_acct = Github(github_token)
    gh_user = gh_acct.get_user()
    for repo in gh_user.get_repos():
        if github_org in repo.full_name:
            all_repos.append(repo.name)
            print("Unwatching %s" % repo.full_name)
            gh_user.remove_from_watched(repo)


if __name__ == '__main__':
    # This function parses and return arguments passed in
    # Assign description to the help doc
    PARSER = argparse.ArgumentParser(
        description="Unwatch all repos in a GitHub org")
    # Add arguments
    PARSER.add_argument(
        '-t', '--Token', type=str, help='GitHub PAT', required=True)
    PARSER.add_argument(
        '-o', '--Organization', type=str, help='GitHub Org', required=True)
    # Array for all arguments passed to script
    ARGS = PARSER.parse_args()
    # Assign args to variables
    ARG_GH_TOKEN = ARGS.Token
    ARG_GH_ORG = ARGS.Organization
    main(ARG_GH_TOKEN, ARG_GH_ORG)
