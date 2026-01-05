# This file is for various helper and utility user CLI function(s) needed.

from copy import deepcopy
from datetime import datetime

from delivery_status_enum import DeliveryStatus

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