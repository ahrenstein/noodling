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

# Use the quiet (-q) flags so we only ever get IDs, regardless of how
# Docker formats its human-readable table output.

echo "Killing and deleting all containers..."
containers=$(docker ps -aq)
if [ -n "$containers" ]; then
  docker rm --force $containers
fi

echo "Deleting all images..."
images=$(docker images -aq | sort -u)
if [ -n "$images" ]; then
  docker rmi --force $images
fi
