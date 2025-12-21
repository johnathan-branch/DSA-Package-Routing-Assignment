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


def is_early_delivery(package):
    return "eod" not in package.delivery_deadline.lower()


def must_be_in_list1(package, early_delivery_counter, delayed_note):
    return (is_early_delivery(package) and early_delivery_counter % 2 == 0) or (delayed_note in package.special_notes.lower())


def must_be_in_list2(package, early_delivery_counter, grouped_package_ids, truck2_only_note):
    return (is_early_delivery(package) and early_delivery_counter % 2 == 1) or (package.package_id in grouped_package_ids) or (package.special_notes.lower() in truck2_only_note) 


def insert_package_with_swap_if_required(target_list, overflow_list, package, list_max_size, must_stay_conditional):
    if len(target_list) < list_max_size:
        target_list.append(package)
        return True

    for i, package_in_target_list in enumerate(target_list):
        if not must_stay_conditional(package_in_target_list):
            overflow_list.append(package_in_target_list)
            target_list[i] = package
            return True

    return False


def fix_wrong_address(package):
    package.address = "410 S State St"
    package.special_notes += "---fixed address---must be delivered after 10:20"


def sort_route1(packages_list):
    # each sort pushes matching condition to the back of the list
    packages_list.sort(key=lambda package: package.delivery_deadline.lower() == "10:30 am")   
    packages_list.sort(key=lambda package: package.delivery_deadline.lower() == "eod")


def sort_route2(packages_list, delayed_note):
    # each sort pushes matching condition to the back of the list
    packages_list.sort(key=lambda package: package.delivery_deadline.lower() == "9:00 am")  
    packages_list.sort(key=lambda package: package.delivery_deadline.lower() == "10:30 am")  
    packages_list.sort(key=lambda package: package.special_notes.lower() == delayed_note.lower())   
    packages_list.sort(key=lambda package: package.delivery_deadline.lower() == "eod")


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
    GROUPED_PACKAGE_IDS = {13, 14, 15, 16, 19, 20} # per the delivery instructions these package IDs need to be delivered together
    TRUCK_2_ONLY_NOTE = "can only be on truck 2"
    WRONG_ADDRESS_LISTED_NOTE = "wrong address listed"
    DELAYED_NOTE = "delayed on flight---will not arrive to depot until 9:05 am"

    packages_list1, packages_list2, packages_list3 = [], [], []
    early_delivery_counter = 0

    for i in range(1, num_of_packages+1):
        package = package_hash_table.lookup(i)
        if package is None:
            continue

        if is_early_delivery(package): early_delivery_counter += 1
        
        if must_be_in_list2(package, early_delivery_counter, grouped_package_ids=GROUPED_PACKAGE_IDS, truck2_only_note=TRUCK_2_ONLY_NOTE):
            inserted = insert_package_with_swap_if_required(
                target_list=packages_list2,
                overflow_list=packages_list3,
                package=package,
                list_max_size=list_max_size,
                must_stay_conditional=lambda p: is_early_delivery(p) or p.package_id in GROUPED_PACKAGE_IDS or TRUCK_2_ONLY_NOTE in p.special_notes.lower()
            )
            if inserted: continue

        if must_be_in_list1(package, early_delivery_counter, delayed_note=DELAYED_NOTE):
            inserted = insert_package_with_swap_if_required(
                target_list=packages_list1,
                overflow_list=packages_list3,
                package=package,
                list_max_size=list_max_size,
                must_stay_conditional=lambda p: is_early_delivery(p) or DELAYED_NOTE in p.special_notes.lower()
            )
            if inserted: continue
        
        if WRONG_ADDRESS_LISTED_NOTE in package.special_notes.lower():
            fix_wrong_address(package)
            packages_list3.append(package) # force this one to be put on truck 3 since it has to be delivered after 10:20 AM 
            continue

        if len(packages_list1) < list_max_size:
            packages_list1.append(package)
        
        elif len(packages_list2) < list_max_size:
            packages_list2.append(package)
        
        else:
           packages_list3.append(package)  

    # after for-loop, sort each list by filtering delivery_deadline and special_notes (for delay note)
    sort_route1(packages_list1)
    sort_route2(packages_list2, delayed_note=DELAYED_NOTE)
    packages_list3.sort(key=lambda package: package.delivery_deadline.lower() == "eod")

    return packages_list1, packages_list2, packages_list3


def user_cli(package_hash_table, user_time, num_of_packages=40):
    """This function serves as the user command line interface to check package statuses at a given provided user time.

    Args:
        package_hash_table (PackageHashTable): The hash table containing the Packages objects.
        user_time (str): Time provided by the user in (HH:MM) 24-hour format.
        num_of_packages (int): Total number of packages in the PackageHashTable object.

    Return: None
    """
    DELAYED_PACKAGES_SET = {6, 25, 28, 32}
    DELAYED_DATETIME = datetime(2025, 1, 1, 9, 5, 0)
    INCORRECT_ADDRESS_CORRECTION_DATETIME = datetime(2025, 1, 1, 10, 20, 0)
    INCORRECT_ADDRESS = "300 State St"
    INCORRECT_ADDRESS_SPECIAL_NOTE = "Wrong address listed"
    INCORRECT_ADDRESS_PACKAGE_ID = 9

    user_time_to_datetime = datetime(2025, 1, 1, int(user_time[:2]), int(user_time[3:]), 0)
    print("")

    for i in range(1, num_of_packages+1):
        original_package = package_hash_table.lookup(i)
        
        if original_package is None:
            continue
        
        package = deepcopy(original_package)

        if package.delivery_time > user_time_to_datetime:
            package.delivery_status = DeliveryStatus.NOT_DELIVERED
            package.delivery_time = None
        
        if (package.package_id in DELAYED_PACKAGES_SET) and (user_time_to_datetime < DELAYED_DATETIME):
            package.delivery_status = DeliveryStatus.DELAYED
            package.delivery_time = None

        if (package.package_id == INCORRECT_ADDRESS_PACKAGE_ID) and (user_time_to_datetime < INCORRECT_ADDRESS_CORRECTION_DATETIME):
            package.address = INCORRECT_ADDRESS
            package.special_notes = INCORRECT_ADDRESS_SPECIAL_NOTE
            package.delivery_status = DeliveryStatus.NOT_DELIVERED
            package.delivery_time = None
        
        print(package)