#!/bin/bash
#
# Bash Script:: dockerClean.sh
#
# Copyright 2020, Matthew Ahrenstein, All Rights Reserved.
#
# Maintainers:
# - Matthew Ahrenstein: @ahrenstein
#
# See LICENSE
#

echo "Killing and deleting all containers..."
for i in `docker ps -a | awk '{print $1}' | grep -v CONTAIN`; do docker kill $i; docker rm $i; done
echo "Deleting all images..."
for i in `docker images | awk '{print $3}' | grep -v IMAGE`; do docker rmi --force $i; done
