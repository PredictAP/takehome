#!/bin/bash

base_directory="test-data"
index_file="index.json"

function create_index {
    local base_dir=$1
    local index=$2

    declare -A index_array

    while IFS= read -r -d '' file_path; do
        file_name=$(basename "$file_path")
        file_size=$(stat -c%s "$file_path")
        content_type=$(file -b --mime-type "$file_path")

        index_array["$file_name"]="{\"size\": $file_size, \"content_type\": \"$content_type\"}"
    done < <(find "$base_dir" -type f -print0)

    index_json="{"
    for key in "${!index_array[@]}"; do
        index_json+="\"$key\": ${index_array[$key]},"
    done
    index_json="${index_json%,}}"
    
    echo "$index_json" > "$index"
}

function lookup_file {
    local index=$1
    local file_name=$2

    if [ -f "$index" ]; then
        file_info=$(jq -r ".[\"$file_name\"]" "$index")
        if [ "$file_info" != "null" ]; then
            echo "$file_info"
        else
            echo "File '$file_name' not found in the index."
        fi
    else
        echo "Index file not found."
    fi
}

# Create the index file
create_index "$base_directory" "$index_file"

# Lookup a file by name
file_name="user1.json"
file_info=$(lookup_file "$index_file" "$file_name")
if [ -n "$file_info" ]; then
    size=$(jq -r ".size" <<< "$file_info")
    content_type=$(jq -r ".content_type" <<< "$file_info")

    echo "File Name: $file_name"
    echo "Size: $size bytes"
    echo "Content Type: $content_type"
fi
