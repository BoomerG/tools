import os
import csv
import sys

# Functions
## Make sure file name is given when executing python program
def file_check():
    file_path = sys.argv[1]
    if len(sys.argv) != 2:
        print("Usage: python csv_reader.py <path_to_csv_file>")
        sys.exit(1)
    if not os.path.isfile(file_path) or not file_path.endswith('.csv'):
        print("Error: The file must exist and be a CSV file.")
        sys.exit(1)
    print(f"Processing file: {file_path}")
    return file_path

## Read in the csv file, print csv headers, give one-line example of data in the file
def read_and_show_example(file_path):
    with open(file_path, mode = 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        example_row = next(reader)

        print("\nHeaders: \n")
        for i, head in enumerate(header):
            print(f'{[i +1]} {head}\t\t{example_row[i]}')
        else:
            for i, head in enumerate(header):
                print(f'{[i + 1]} {head}\t\t"none"')
        return header

## Have user select what headers he wants to extract and in what order
def select_headers(header):
    while True:
        print("\nWhich fields wouold you like to focus on? (Enter field numbers separated by commas, e.g., 1,3,4)")
        raw_input = input()
        choices = [choice.strip() for choice in raw_input.split(',')]
        if any(not choice for choice in choices):
            print("Error: All choices must be non-empty.")
            continue
        if any(char not in {',', ''} and not char.isalnum() for char in raw_input):
            print("Error: Incorrect delimiter. Enter field numbers separated by commas, e.g., 1,3,4")
            continue
        selected_fields = [header[int(choice.strip()) -1] for choice in choices]
        return selected_fields

## Ask for out_file path/name
def out_file():
    while True:
        out_file = input("\nWhat is the output file path?: ")
        if os.path.isfile(out_file):
            return out_file
        else:
            if not out_file.endswith('.csv'):
                print("Error: The file must be a CSV file.")
                continue
            return out_file

## Create new csv file that is filtered exactly the way the user wants the data formated (in csv)
def create_filtered_csv(file_path, selected_fields, output_file_path):
    with open(file_path, mode = 'r') as infile, open(output_file_path, mode = 'w', newline = '') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames = selected_fields)
        writer.writeheader()
        for row in reader:
            writer.writerow({field: row[field] for field in selected_fields})


# Main program
def main():
    try:
        while True:
            print("Running... Press Ctrl+C to exit.\n")
            file_path = file_check()
            header = read_and_show_example(file_path)
            selected_fields = select_headers(header)
            output_file_path = out_file()
            create_filtered_csv(file_path, selected_fields, output_file_path)
    except KeyboardInterrupt:
        print("Program exited by user.")

# Run main program
main()
