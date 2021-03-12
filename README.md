Noodling
========
This is just a random scripts and config files repo where I keep code I'm playing with that doesn't deserve its own repo.  
This repo is named after Ian Grimm's hated phrase "Let me noodle on this" because I found it funny.

![noodle](images/iangrimm.png)

Scripts in repo
---------------
Currently the following scripts are in the repo:

1. [GitHub Unfollow](python/unfollow_github_org.py) - A quick python script to unfollow all repos in a GitHub org
2. [encrypt_data_bag.rb](ruby/encrypt_data_bag.rb) and [decrypt_data_bag.rb](ruby/decrypt_data_bag.rb) - Encrypt and
decrypt Chef databags locally.
3. [dockerClean.sh](bash/dockerClean.sh) - Delete all local docker containers and images.
4. [Download Apple Music Playlists](applescript/downloadAppleMusicPlaylists.scpt) - A simple Apple Script to download
all of my playlists for offline listening on macOS while I wait for Apple to fix the missing "Download" right click
context menu item.
5. [pug_finder.py](python/pug_finder.py) - A simple script that searches a Google Sheet's pubhtml URL for the string "PUG".
It emails the results via AWS SES using SMTP
6. [crypto_functions.py](python/crypto_functions.py) - A small library for cryptocurrency functions.
7. [crypto_pricing.py](python/crypto_pricing.py) - A script that manages a specific Google sheet I own regarding crypto prices.
Config files in this repo
7. [list_coinbase_pro_txs.py](python/list_coinbase_pro_txs.py) - A simple script to list the last 24 ours of Coinbase Pro transactions.

-------------------------
Some config files I want to preserve:

1. [Duo LDAP Proxy for JumpCloud](configFiles/authproxy.cfg) - A Duo LDAP Proxy configuration that uses JumpCloud as the
2. [okta_ldap_nginx.conf](configFiles/okta_ldap_nginx.conf) - An NginX configuration to authenticate against Okta's LDAP proxy
3. [Visual Studio Config](configFiles/VS_CSharp.vssettings) - My settings for coding C# in Visual Studio
upstream LDAP server
4. [VSCode Settings](configFiles/vscode.settings.json) - My settings for VSCode
    1. [VSCode Extensions](docs/VSCodeExtensions.md) - VSCode extensions I use with the above config
5. [Nintendo Switch Connection Test](configFiles/nginx_switch_connection_test.conf) - NginX site to spoof the Nintendo Switch's
"I can reach the internet" test page
6. [My Mac zsh config](zsh/mac-zshrc) - My macOS zsh configuration contained in a single file
    1. [fzf config](zsh/fzf.zsh) - The `~/.fzf.zsh` configuration file that pairs with my Mac zsh config

Other files in this repo
------------------------
Any other files that are useful:

1. [Standard gitignore](.gitignore) - My usual .gitignore file (Also used by this repo)
2. [pre-commit configuration](.pre-commit-config.yaml) - The configuration used by GitHub actions to enforce pre-commit

pre-commit
----------
This repo uses Yelp's [pre-commit](https://pre-commit.com/) to manage some pre-commit hooks automatically.  
In order to use the hooks, make sure you have `pre-commit` in your `$PATH`.  
Once in your path you should run `pre-commit install` in order to configure it. If you push commits that fail pre-commit, your PR will
not pass tests.

Why not gists?
--------------
The main reason is because gists have a different URL every time they are updated while
`https://github.com/ahrenstein/noodling/blob/master/.gitignore` will never change no matter how often I update it.
This makes pulling these files via scripts reliable.
