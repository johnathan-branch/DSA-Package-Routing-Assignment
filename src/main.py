# J.BRANCH, WGU Student ID No: 012206114

from pathlib import Path

from package_hash_table import PackageHashTable
from utility import *

# project root folder is parent of the current working directory
ROOT_DIR = Path.cwd().parent 
PACKAGE_CSV_FILEPATH = str(ROOT_DIR) + "\\resources\\WGUPS Package File.csv"
DISTANCE_CSV_FILEPATH = str(ROOT_DIR) + "\\resources\\WGUPS Distance Table.csv"
 

def main():
    # read the package file and populate hash table (Step 1)
    package_csv_file_data = read_and_parse_csv_file(file_path=PACKAGE_CSV_FILEPATH)
    package_hash_table = PackageHashTable(size=10)
    populate_package_hash_table(package_hash_table, package_data=package_csv_file_data)

    # create 2 data structures: 1 for the distance data and another to map addresses to location distances (Step 2)
    distance_data, address_location_map = read_and_parse_distance_file(file_path=DISTANCE_CSV_FILEPATH)

    # partition packages into 3 separate list (a.k.a loading the 'trucks')
    package_list1, package_list2, package_list3 = partition_packages(package_hash_table, list_max_size=14, num_of_packages=40)

    # Step 1 debug print statements: (covers requirements A and B)
    #print(package_hash_table)
    #print(package_hash_table.lookup(32))

    # Step 2 debug print statements: (covers part of requirement C)
    #print(distance_data[2][1]) # Should be distance between Int'l Peace Gardens and Sugar House Park (7.1)
    #print(address_location_map["1060 Dalton Ave S"]) # This hard-coded string should return index 1

    # Step 3 debug print statements: (covers part of requirement C)
    #print(package_list1, package_list2, package_list3, sep="\n\n")


if __name__ == "__main__":
    main()