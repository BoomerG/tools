import os
import csv
import sys

def file_check():
    if len(sys.argv) != 2:
        print("Usage: python csv_reader.py <path_to_csv_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.isfile(file_path) or not file_path.endswith('.csv'):
        print("Error: The file must exist and be a CSV file.")
        sys.exit(1)
    
    print(f"Processing file: {file_path}")
    return file_path

def read_and_show_example(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        header = next(reader)
        example_row = next(reader, None)

        # Calculate the maximum header length for uniform indentation
        max_len = max(len(head.strip().strip('"')) for head in header)

        print("\nHeaders:\n")
        if example_row:
            for i, head in enumerate(header):
                head_cleaned = head.strip().strip('"')
                value_cleaned = example_row[i].strip().strip('"')
                print(f'{i + 1}. {head_cleaned:<{max_len}}    {value_cleaned}')
        else:
            for i, head in enumerate(header):
                head_cleaned = head.strip().strip('"')
                print(f'{i + 1}. {head_cleaned:<{max_len}}    {"none"}')

        return [h.strip().strip('"') for h in header]

def select_headers(header):
    while True:
        print("\nWhich fields would you like to focus on? (Enter field numbers separated by commas, e.g., 1,3,4)")
        raw_input = input().strip()
        choices = [choice.strip() for choice in raw_input.split(',')]

        if any(not choice.isdigit() for choice in choices):
            print("Error: All choices must be valid numbers.")
            continue

        selected_indices = [int(choice) - 1 for choice in choices if choice.isdigit() and 0 <= int(choice) - 1 < len(header)]
        if not selected_indices:
            print("Error: Invalid field numbers.")
            continue

        selected_fields = [header[index] for index in selected_indices]
        return selected_fields

def get_output_file():
    while True:
        output_file_path = input("\nWhat is the output file path?: ").strip()
        if not output_file_path.endswith('.csv'):
            print("Error: The file must be a CSV file.")
            continue
        return output_file_path

def create_filtered_csv(file_path, selected_fields, output_file_path):
    with open(file_path, mode='r') as infile, open(output_file_path, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        # Strip whitespace and quotes from the header
        reader.fieldnames = [field.strip().strip('"') for field in reader.fieldnames]
        writer = csv.DictWriter(outfile, fieldnames=selected_fields, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in reader:
            writer.writerow({field: row[field].strip().strip('"') for field in selected_fields})

def main():
    try:
        print("Running... Press Ctrl+C to exit.\n")
        file_path = file_check()
        header = read_and_show_example(file_path)
        selected_fields = select_headers(header)
        output_file_path = get_output_file()
        create_filtered_csv(file_path, selected_fields, output_file_path)
        print("Filtered CSV created successfully.")
    except KeyboardInterrupt:
        print("\nProgram exited by user.")
    except KeyError as e:
        print(f"Error: Field {e} not found in the input CSV. Please check the field names.")

if __name__ == "__main__":
    main()
