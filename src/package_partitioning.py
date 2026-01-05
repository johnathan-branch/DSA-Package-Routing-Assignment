# This file is for various helper and utility package partitioning functions needed.

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