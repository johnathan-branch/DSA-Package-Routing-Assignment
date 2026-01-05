# This file is for various helper and utility file IO and parsing functions needed.

from package import Package

def read_and_parse_csv_file(file_path):
    """Reads and parses a standard CSV file.

    Args:
        file_path (string): Full path to the CSV file to parse.

    Returns:
        lines (list[list(str)]): A nested list of the parsed data.
    """
    lines = []

    with open(file_path) as f:
        for line in f:
            lines.append([line])

    return lines 


def populate_package_hash_table(package_hash_table, package_data):
    """This function takes in a package_hash_table object and package_data as arguments and inserts the package_data fields into the table object.

        Args:
            package_hash_table (Package): Package object to populate.
            package_data (list[list[str]]): Data to populate the package object with, fields must be in correct order.
        
        Returns:
            None: 
    """
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


def read_and_parse_distance_file(file_path):
    """This function takes in the file_path argument to the cleaned distance file (CSV file) and returns two data structures.

        Args:
            file_path (str): Full path to the CSV file to parse.
        
        Returns:
            distance_data (list[list[float]]): A nested list of list with float values for the distance data.
            
            address_location_map (dict[str]): A dictionary where the key is the address and value is the associated index for that address in the distance_data. 
    """
    distance_data = []
    address_location_map = {}

    with open(file_path) as f:
        for idx, line in enumerate(f):
            col_data = line.split(",")
            address_location_map[col_data.pop(0)] = idx
            distance_data.append([float(x) for x in col_data])

    return distance_data, address_location_map