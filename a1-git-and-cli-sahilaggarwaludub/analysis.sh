#!/usr/bin/env bash 
## analysis.sh
cd sonnets
touch sonnets.txt
# Download the sonnets
curl http://www.gutenberg.org/files/1041/1041.txt > sonnets.txt


# Trim introduction and concluding lines

tail -n 2986 sonnets.txt| head -n 2618 > cleaned-sonnets.txt

# Remove leading blank characters 
cut -c 3-70 cleaned-sonnets.txt > cleaned_sonnets.txt
 
# Split sonnets into individual files. This will involve *many* commands.
split -l 1667 cleaned_sonnets.txt
split -l 17 xaa sonnet-
split -l 475 xab sonnet-x-
split -l 17 sonnet-x-aa sonnet-1-
split -l 17 sonnet-x-ab sonnet-127-
tail -n 17 xab > sonnet-127-bb
rm x{aa,ab}
rm sonnet-x-{aa,ab,ac}
rm sonnet-du
# Find the longest sonnet (most words)
rm lengths.txt
wc -w sonnet-* > lengths1.txt
sort -r lengths1.txt > lengths.txt

# Search for specific words in  the sonnets
grep truth sonnet-* > truth.txt
grep love *a > love.txt
