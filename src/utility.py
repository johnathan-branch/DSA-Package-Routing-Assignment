# This file is for various helpers or utility functions needed.

from package import Package

def read_and_parse_csv_file(file_path):
    lines = []

    with open(file_path) as f:
        for line in f:
            lines.append([line])

    return lines 


def populate_package_hash_table(package_hash_table, package_data):

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