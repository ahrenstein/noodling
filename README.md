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

Config files in this repo
-------------------------
Some config files I want to preserve:

1. [Duo LDAP Proxy for JumpCloud](configFiles/authproxy.cfg) - A Duo LDAP Proxy configuration that uses JumpCloud as the
2. [okta_ldap_nginx.conf](configFiles/okta_ldap_nginx.conf) - An NginX configuration to authenticate against Okta's LDAP proxy
3. [Visual Studio Config](configFiles/VS_CSharp.vssettings) - My settings for coding C# in Visual Studio
upstream LDAP server
4. [VSCode Settings](configFiles/vscode.settings.json) - My settings for VSCode
    1. [VSCode Extensions](docs/VSCodeExtensions.md) - VSCode extensions I use with the above config

Other files in this repo
------------------------
Any other files that are useful:

1. [Standard gitignore](.gitignore) - My usual .gitignore file (Also used by this repo)

Why not gists?
--------------
The main reason is because gists have a different URL every time they are updated while
`https://github.com/ahrenstein/noodling/blob/master/.gitignore` will never change no matter how often I update it.
This makes pulling these files via scripts reliable.
