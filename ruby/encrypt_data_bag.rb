#!/usr/bin/env ruby
#
# Ruby Script:: encrypt_data_bag.rb
#
# Copyright 2020, Matthew Ahrenstein, All Rights Reserved.
#
# Maintainers:
# - Matthew Ahrenstein: @ahrenstein
#
# See LICENSE
#

if ARGV.length < 2
  puts "usage: #{$0} databag.json new_encrypted_databag.json [encrypted_data_bag_secret]"
  exit(1)
end

databag_file = ARGV[0]
out_file = ARGV[1]
if ARGV.length >= 3
  secret_file = ARGV[2]
end

require 'rubygems'
require 'json'
require 'chef/encrypted_data_bag_item'
require 'highline/import'

puts "Load #{databag_file}"
data = JSON.parse(File.read(databag_file))

if secret_file
  secret = Chef::EncryptedDataBagItem.load_secret secret_file
else
  secret = ask("Enter databag secret: ") { |q| q.echo = false }
end
unless secret && secret.length > 0 # could enforce secret length
  puts "You must provide a secret password"
  exit(2)
end
encrypted_data = Chef::EncryptedDataBagItem.encrypt_data_bag_item(data, secret)

puts "Write encrypted #{out_file}"
File.open(out_file, 'w') do |f|
  f.print JSON.pretty_generate(encrypted_data)
end
