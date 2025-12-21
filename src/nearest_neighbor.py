from datetime import datetime, timedelta

from delivery_status_enum import DeliveryStatus

def package_nearest_neighbor_algorithm(package_list, dist_data, address_loc_map, package_hash_table, start_time=datetime(2025, 1, 1, 8, 0, 0), speed_mph=18.0, delivery_truck_no=1):
    """This functions takes in a list of packages and a start time as arguments, and uses a nearest-neighbor implementation to deliver the packages. 

        Args:
            package_list (list[Package]): List of packages on a given delivery route.
            dist_data (list[list[float]]): A nested list of list with float values for the distance data. 
            address_loc_map (dict[str]): A dictionary where the key is the address and value is the associated index for that address in the distance_data.  
            start_time (datetime object): Start time of the delivery route (default datetime of 2025/01/01 8:00:00).
            speed_mph (float): Default of 18.0.
            delivery_truck_no (integer): Default of 1.


        Returns:
            route_time (datetime object): The time after execution of the of the delivery route. 
            route_distance (float): The total distance travelled on the route.
    """

    """
        High-level pseudo-code:
            - Find the packages in the list that has the address that is closest to the current route location.
            - Move to that address
            - Deliver
            - Repeat until all packages have been delivered
    """
    route_location_idx = 0 # we always start our route at zero (a.k.a the Hub)
    route_distance = 0.0 # initialize cumulative_distance to 0.0
    route_time = start_time # initialize cumulative_time with the value from the start_time argument
    
    while len(package_list) > 0:
        # Separate urgent packages (non-EOD deadlines)
        urgent_packages = [p for p in package_list if "eod" not in p.delivery_deadline.lower()]
        
        if urgent_packages:
            candidates = [p for p in urgent_packages if "9:00 am" in p.delivery_deadline.lower()]
            
            if len(candidates) == 0:
                candidates = [
                    p for p in urgent_packages
                    if ("Delayed on flight---will not arrive to depot until 9:05 am".lower() not in p.special_notes.lower())
                    or route_time > datetime(2025, 1, 1, 9, 5, 0)
                ]
        else:
            candidates = package_list

        package_idx_to_pop = None
        shortest_dist_package_lookup_id = None
        shortest_distance = float("inf")
        shortest_route_location_idx = None
        
        # This for-loop accomplishes finding the shortest distance package (*only if delivery_deadline doesn't matter)
        for package_list_idx, package in enumerate(package_list):
            if package not in candidates:
                continue # skip non-candidates at first (eventually will get to the non-candidates)

            package_in_hash_table = package_hash_table.lookup(package.package_id)
            if package_in_hash_table: package_in_hash_table.delivery_status = DeliveryStatus.EN_ROUTE

            package_location_idx = address_loc_map[package.address]

            if route_location_idx < package_location_idx:
                package_distance = dist_data[package_location_idx][route_location_idx]
            else:
                package_distance = dist_data[route_location_idx][package_location_idx]
            
            if (package_distance < shortest_distance):
                shortest_distance = package_distance
                shortest_route_location_idx = package_location_idx
                shortest_dist_package_lookup_id = package.package_id
                package_idx_to_pop = package_list_idx
            
        # Now that we found the shortest distance, we need to deliver that package
        route_location_idx = shortest_route_location_idx
        time_to_deliver_seconds = (shortest_distance * 3600.0) / speed_mph
        
        if time_to_deliver_seconds < 0.0:     
            raise ValueError(f"Invalid time to deliver calculated. ({time_to_deliver_seconds})\n")
        
        route_time += timedelta(seconds=time_to_deliver_seconds)
        route_distance += shortest_distance

        # Update the package delivery status in our data source (package_hash_table)
        package_to_update = package_hash_table.lookup(shortest_dist_package_lookup_id)

        if package_to_update:
            package_to_update.delivery_status = DeliveryStatus.DELIVERED
            package_to_update.delivery_time = route_time
            package_to_update.delivery_truck_no = delivery_truck_no

        # Pop off that package from the list, now that it has been delivered
        package_list.pop(package_idx_to_pop)
    
    return route_time, route_distance