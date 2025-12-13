# J.BRANCH, WGU Student ID No: 012206114

from pathlib import Path

from hash_table import PackageHashTable
from utility import *

# project root folder is parent of the current working directory
ROOT_DIR = Path.cwd().parent 
PACKAGE_CSV_FILEPATH = str(ROOT_DIR) + "\\resources\\WGUPS Package File.csv"
DISTANCE_CSV_FILEPATH = str(ROOT_DIR) + "\\resources\\WGUPS Distance Table.csv"
 

def main():
    # create package hash table
    package_hash_table = PackageHashTable(size=10)

    # read the package file and populate hash table (Step 1)
    package_csv_file_data = read_and_parse_csv_file(file_path=PACKAGE_CSV_FILEPATH)
    package_hash_table = populate_package_hash_table(package_data=package_csv_file_data)

    # Step 1 debug tests (covers requirements A and B)
    #print(package_hash_table)
    #print(package_hash_table.lookup(32))

    # create 2 data structures: 1 for the distance data and another to map address to locations (Step 2)
    distance_data = []
    address_location_map = {}



if __name__ == "__main__":
    main()