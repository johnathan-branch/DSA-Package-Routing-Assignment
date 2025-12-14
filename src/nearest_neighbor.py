from datetime import datetime, timedelta

from package import Package

def package_nearest_neighbor_algorithm(package_list, dist_data, address_loc_map, start_time=datetime(2025, 1, 1, 8, 0, 0)):
    """This functions takes in a list of packages and a start time as arguments, and uses a nearest-neighbor implementation to deliver the packages. 

        Args:
            package_list (list[Package]): List of packages on a given delivery route.
            dist_data (list[list[float]]): A nested list of list with float values for the distance data. 
            address_loc_map (dict[str]): A dictionary where the key is the address and value is the associated index for that address in the distance_data.  
            start_time (datetime object): Start time of the delivery route (default datetime of 2025/01/01 8:00:00).

        Returns:
            cumulative_time (datetime object): The time after execution of the of the delivery route. 
    """

    """
        High-level pseudo-code:
            - Find the packages in the list that has the address that is closest to the current route location.
            - Move to that address
            - Deliver
            - Repeat until all packages have been delivered
    """
    current_location = 0.0 # we always start our route at zero (a.k.a the Hub)
