#!/bin/sh
find data -type f -size +500k -exec ls -l -s {} \; | sort -n |  awk '{ print $1 " KB " $10 }'
