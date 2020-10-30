#!/bin/sh
# source this file
export API_TOKEN=`cat /tmp/setup-all.sh.out | grep apiToken | jq .data.apiToken | tr -d \"`
