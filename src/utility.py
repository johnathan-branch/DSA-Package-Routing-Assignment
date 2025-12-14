# This file is for various helper and utility functions needed.

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


def partition_packages(package_hash_table, list_max_size=14, num_of_packages=40):
    """This function takes the package_hash_table in as an argument and partitions the packages into 3 lists.
       Partitioning is done with following all of the constraints listed in the special notes of the Package objects. 

    Args:
        package_hash_table (PackageHashTable): The hash table containing the Packages objects to partition into lists.
        list_max_size (int): Max size of each output list.
        num_of_packages (int): Total number of packages to partition.

    Return:
        packages_list1: List of packages on route 1.

        packages_list2: List of packages on route 2.
        
        packages_list3: List of packages on route 3.
    """
    packages_list1, packages_list2, packages_list3 = [], [], []

    for i in range(1, num_of_packages+1):
        package = package_hash_table.lookup(i)

        if package is None:
            continue

        else:
            delivery_must_be_in_list2 = package.package_id in (13, 14, 15, 16, 19, 20) or "Can only be on truck 2".lower() in package.special_notes.lower()
            if delivery_must_be_in_list2:
               # per the delivery instructions, (13, 14, 15, 16, 19, 20) all need to be delivered together

                if len(packages_list2) < list_max_size:
                    packages_list2.append(package)
                else:
                    for i in range(len(packages_list2)):
                        delivery_must_be_in_list2 = packages_list2[i].package_id in (13, 14, 15, 16, 19, 20) or "Can only be on truck 2".lower() in packages_list2[i].special_notes.lower()
                        if not delivery_must_be_in_list2:
                            packages_list3.append(packages_list2[i])
                            packages_list2[i] = package
                            break
                continue

            elif "Wrong address listed".lower() in package.special_notes.lower():
                package.address = "410 S State St"
                package.special_notes += "---fixed address---must be delivered after 10:20"

            if len(packages_list1) < list_max_size:
                packages_list1.append(package)
            elif len(packages_list2) < list_max_size:
                packages_list2.append(package)
            else:
               packages_list3.append(package)  

    # after for-loop, lazy-sort each list by filtering EOD deliveries to the end (ignore other times for now)      
    packages_list1.sort(key=lambda package: package.delivery_deadline == "EOD")
    packages_list2.sort(key=lambda package: package.delivery_deadline == "EOD")
    packages_list3.sort(key=lambda package: package.delivery_deadline == "EOD")

    return packages_list1, packages_list2, packages_list3