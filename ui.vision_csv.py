import argparse
import os

def format_csv_data(csvData):
    data = [line.split(',') for line in csvData.strip().split('\n')]
    formattedCsvData = '\n'.join([','.join(row) for row in data])
    return formattedCsvData.replace('\\n', '\n')

def write_csv_data_to_file(path, var, csvData):
    filename = os.path.join(path, "datasources", var)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(format_csv_data(csvData))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, help="Path to uivision folder")
    parser.add_argument("--var3", type=str, help="CSV file name")
    parser.add_argument("--csvData", type=str, help="CSV data to write to file")

    args = parser.parse_args()

    write_csv_data_to_file(args.path, args.var3, args.csvData)