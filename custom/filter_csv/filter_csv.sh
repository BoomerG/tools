#!/bin/bash

# Check if a file was passed
if [ -z "$1" ]; then
  echo "Usage: $0 <csv_file>"
  exit 1
fi

input_csv="$1"

# Read headers
IFS=',' read -r -a headers < <(head -n 1 "$input_csv")

echo "Available headers:"
for i in "${!headers[@]}"; do
  echo "$i) ${headers[$i]}"
done

echo "Enter the numbers of the headers you want to keep (comma-separated, e.g., 0,2,3):"
read -r selected

IFS=',' read -r -a indices <<< "$selected"

# Construct cut-style column list (1-based)
cut_list=""
for index in "${indices[@]}"; do
  cut_index=$((index + 1))
  cut_list+="$cut_index,"
done
cut_list="${cut_list%,}"  # Remove trailing comma

# Output file
output_csv="filtered_output.csv"

# Create new CSV with selected columns
cut -d',' -f"$cut_list" "$input_csv" > "$output_csv"

echo "Filtered CSV saved as: $output_csv"

