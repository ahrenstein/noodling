#!/usr/bin/env ruby
#
# Ruby Script:: decrypt_data_bag.rb
#
# Copyright 2020, Matthew Ahrenstein, All Rights Reserved.
#
# Maintainers:
# - Matthew Ahrenstein: @ahrenstein
#
# See LICENSE
#

if ARGV.length < 2
  puts "usage: #{$0} encrypted_databag.json new_unencrypted_databag.json [encrypted_data_bag_secret]"
  exit(1)
end


require 'chef/encrypted_data_bag_item'
require 'json'

keyfile = ARGV[2]
out_file = ARGV[1]
encrypted_path = ARGV[0]

secret = Chef::EncryptedDataBagItem.load_secret(keyfile)

encrypted_data = JSON.parse(File.read(encrypted_path))

plain_data = Chef::EncryptedDataBagItem.new(encrypted_data, secret).to_hash

File.open(out_file, 'w') do |f|
  f.print JSON.pretty_generate(plain_data)
end
