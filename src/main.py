from pathlib import Path

from package import Package
from hash_table import PackageHashTable

# project root folder is parent of the current working directory
ROOT_DIR = Path.cwd().parent 
PACKAGE_CSV_FILEPATH = str(ROOT_DIR) + "\\resources\\WGUPS Package File.csv"
DISTANCE_CSV_FILEPATH = str(ROOT_DIR) + "\\resources\\WGUPS Distance Table.csv"

def read_and_parse_csv_file(file_path):
    lines = []

    with open(file_path) as f:
        for line in f:
            lines.append([line])

    return lines    


def populate_package_hash_table(package_data):
    package_hash_table = PackageHashTable(size=10)

    for element in package_data:
        line = element[0]
        col_data = line.split(",")[0:8]

        if len(col_data) != 8:
            # Each row of data should have at least eight fields, if not something isn't right. 
            raise Exception("Encountered exception parsing the package file data, please inspect the data source.")

        else:       
            col_data[0] = int(col_data[0])
            col_data[6] = float(col_data[6])
            package_hash_table.insert(Package(*col_data))
    
    return package_hash_table


def main():
    # read the package file and populate hash table (Step 1)
    package_csv_file_data = read_and_parse_csv_file(file_path=PACKAGE_CSV_FILEPATH)
    package_hash_table = populate_package_hash_table(package_data=package_csv_file_data)

    # Step 1 debug tests
    #print(package_hash_table)
    #print(package_hash_table.lookup(32))


if __name__ == "__main__":
    main()