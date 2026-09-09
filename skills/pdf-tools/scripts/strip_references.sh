#!/bin/bash

file="$1"
output_file="${file%.md}_clean.md"

# Find line number where reference section starts
line_num=$(grep -n -i -E "^#{1,6}.*\b(reference|references|bibliography|bibliographies)\b" "$file" | head -1 | cut -d: -f1)

if [ -z "$line_num" ]; then
    cp "$file" "$output_file"
else
    head -n $((line_num - 1)) "$file" > "$output_file"
fi