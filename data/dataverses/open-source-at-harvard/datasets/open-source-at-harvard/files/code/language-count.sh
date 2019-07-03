#!/bin/sh
# Create tab delimited output of language by popularity.
echo "count\tlanguage"
cat data/*tsv | cut -f2 | sed 's/^""$/∅/'  | tr -d '"' | sort | uniq -c | sort -r | while read -r count lang; do echo "$count\t$lang"; done
