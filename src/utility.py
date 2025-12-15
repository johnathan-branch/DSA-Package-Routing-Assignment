# This file is for various helper and utility functions needed.

from copy import deepcopy
from datetime import datetime

from delivery_status_enum import DeliveryStatus
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


def partition_packages(package_hash_table, list_max_size=16, num_of_packages=40):
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
    early_delivery_counter = 0

    for i in range(1, num_of_packages+1):
        package = package_hash_table.lookup(i)

        if package is None:
            continue

        else:
            early_delivery = "EOD".lower() not in package.delivery_deadline.lower()
            if early_delivery: early_delivery_counter += 1
            delivery_must_be_in_list1 = (early_delivery and early_delivery_counter%2 == 0) or package.package_id in (13, 14, 15, 16, 19, 20)
            delivery_must_be_in_list2 = (early_delivery and early_delivery_counter%2 == 1) or "Can only be on truck 2".lower() in package.special_notes.lower()

            if delivery_must_be_in_list1:
                # per the delivery instructions, (13, 14, 15, 16, 19, 20) all need to be delivered together
                if len(packages_list1) < list_max_size:
                    packages_list1.append(package)
                else:
                    for i in range(len(packages_list1)):
                        delivery_must_be_in_list1 =  "EOD".lower() not in packages_list1[i].delivery_deadline.lower() or packages_list1[i].package_id in (13, 14, 15, 16, 19, 20)
                        if not delivery_must_be_in_list1:
                            packages_list3.append(packages_list1[i])
                            packages_list1[i] = package
                            break
                continue
            
            elif delivery_must_be_in_list2:
               
                if len(packages_list2) < list_max_size:
                    packages_list2.append(package)
                else:
                    for i in range(len(packages_list2)):
                        delivery_must_be_in_list2 = "EOD".lower() not in packages_list2[i].delivery_deadline.lower() or "Can only be on truck 2".lower() in packages_list2[i].special_notes.lower()
                        if not delivery_must_be_in_list2:
                            packages_list3.append(packages_list2[i])
                            packages_list2[i] = package
                            break
                continue

            elif "Wrong address listed".lower() in package.special_notes.lower():
                package.address = "410 S State St"
                package.special_notes += "---fixed address---must be delivered after 10:20"
                packages_list3.append(package) # put this one route3 since it has to be delivered later on (after 10:20)
                continue

            if len(packages_list1) < list_max_size:
                packages_list1.append(package)
            elif len(packages_list2) < list_max_size:
                packages_list2.append(package)
            else:
               packages_list3.append(package)  

    # after for-loop, lazy-sort each list by filtering delivery_deadline and delays
    packages_list1.sort(key=lambda package: package.delivery_deadline.upper() == "10:30 AM")  
    packages_list1.sort(key=lambda package: package.special_notes.upper() == "Delayed on flight---will not arrive to depot until 9:05 am".upper())   
    packages_list1.sort(key=lambda package: package.delivery_deadline.upper() == "EOD")
    packages_list2.sort(key=lambda package: package.delivery_deadline.upper() == "EOD")
    packages_list3.sort(key=lambda package: package.delivery_deadline.upper() == "EOD")

    return packages_list1, packages_list2, packages_list3


def user_cli(package_hash_table, user_time, num_of_packages=40):
    """This function serves as the user command line interface to check package statuses at a given provided user time.

    Args:
        package_hash_table (PackageHashTable): The hash table containing the Packages objects.
        user_time (str): Time provided by the user in (HH:MM) 24-hour format.
        num_of_packages (int): Total number of packages in the PackageHashTable object.

    Return: None
    """
    user_time_to_datetime = datetime(2025, 1, 1, int(user_time[:2]), int(user_time[3:]), 0)
    print("")

    for i in range(1, num_of_packages+1):
        original_package = package_hash_table.lookup(i)
        
        if original_package is None:
            continue
        
        else:
            package = deepcopy(original_package)

            if package.delivery_time > user_time_to_datetime:
                package.delivery_status = DeliveryStatus.NOT_DELIVERED
                package.delivery_time = None
            
            if package.package_id in (6, 25, 28, 32) and user_time_to_datetime < datetime(2025, 1, 1, 9, 5, 0):
                package.delivery_status = DeliveryStatus.DELAYED
                package.delivery_time = None

            if package.package_id == 9 and user_time_to_datetime < datetime(2025, 1, 1, 10, 20, 0):
                package.address = "300 State St"
                package.special_notes = "Wrong address listed"
                package.delivery_status = DeliveryStatus.NOT_DELIVERED
                package.delivery_time = None
            
            print(package)