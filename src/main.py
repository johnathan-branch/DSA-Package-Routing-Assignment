# J.BRANCH, WGU Student ID No: 012206114

from datetime import datetime
from pathlib import Path

from nearest_neighbor import package_nearest_neighbor_algorithm
from package_hash_table import PackageHashTable
from utility import *

# project root folder is parent of the current working directory
ROOT_DIR = Path.cwd().parent 
#DEBUG_ROOT_DIR = "C:\\WGU-Assignments\C950-DSA_HashTable_Assignment"
PACKAGE_CSV_FILEPATH  = str(ROOT_DIR) + "\\resources\\WGUPS Package File.csv"
DISTANCE_CSV_FILEPATH = str(ROOT_DIR) + "\\resources\\WGUPS Distance Table.csv"
 

def main():
    # read the package file and populate hash table (Step 1)
    package_csv_file_data = read_and_parse_csv_file(file_path=PACKAGE_CSV_FILEPATH)
    package_hash_table = PackageHashTable(size=10)
    populate_package_hash_table(package_hash_table, package_data=package_csv_file_data)

    # create 2 data structures: 1 for the distance data and another to map addresses to location distances (Step 2)
    distance_data, address_location_map = read_and_parse_distance_file(file_path=DISTANCE_CSV_FILEPATH)

    # partition packages into 3 separate list (a.k.a loading the 'trucks')
    # package_list3 can be over list_max_size to accomodate all of delivery constraints handled by package_list1 and package_list2
    package_list1, package_list2, package_list3 = partition_packages(package_hash_table, list_max_size=16, num_of_packages=40)
    
    # Since '3 trucks and 2 drivers' are availible, start 2 trucks close to same time and have last truck start after a driver is 'back'
    # dt - delivery time, dd - delivery distance
    dt1, dd1 = package_nearest_neighbor_algorithm(package_list1, distance_data, address_location_map, package_hash_table, start_time=datetime(2025, 1, 1, 9, 5, 0)) # start at 9:05 to accomodate 'delayed packaged'
    dt2, dd2 = package_nearest_neighbor_algorithm(package_list2, distance_data, address_location_map, package_hash_table, start_time=datetime(2025, 1, 1, 8, 10, 0), delivery_truck_no=2)
    dt3, dd3 = package_nearest_neighbor_algorithm(package_list3[:16], distance_data, address_location_map, package_hash_table, start_time=dt2, delivery_truck_no=3)
    dt4, dd4 = package_nearest_neighbor_algorithm(package_list3[16:], distance_data, address_location_map, package_hash_table, start_time=dt3, delivery_truck_no=3)
    
    final_delivery_time = max(dt1, dt2, dt3, dt4)
    final_delivery_distance = round(dd1 + dd2 + dd3 + dd4, 2)

    print(f"\nFinal package delivery time = {final_delivery_time}, Total distance travelled (mi) = {final_delivery_distance}\n")

    user_time = input("Enter a time in (HH:MM) 24-hour format: ")

    if (len(user_time) == 5 and user_time[2] == ":"): # could do a better regex check here... but lets keep it simple for now
        user_cli(package_hash_table, user_time, num_of_packages=40)
    else:
        print("Invalid format for time given, please run the script again.")

    # --- DEBUG PRINT STATEMENTS --- commented out for program submission
    # Step 1 debug print statements: (covers requirements A and B)
    #print(package_hash_table)
    #print(package_hash_table.lookup(32))

    # Step 2 debug print statements: (covers part of requirement C)
    #print(distance_data[2][1]) # Should be distance between Int'l Peace Gardens and Sugar House Park (7.1)
    #print(address_location_map["1060 Dalton Ave S"]) # This hard-coded string should return index 1
    #print(address_location_map)

    # Step 3 debug print statements {NOTE - These has to be moved up before calling nearest neighbor function}: (covers part of requirement C)
    #print(package_list1, package_list2, package_list3, sep="\n\n")
    #print(len(package_list1), len(package_list2), len(package_list3))


if __name__ == "__main__":
    main()