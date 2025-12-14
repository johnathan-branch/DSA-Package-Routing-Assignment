class PackageHashTable:
    """
        This hashtable implementation is intended to support storing the package objects. 
        It's implemented using a simple list of list, where each inner list
        represents a bucket in the hash table. The key for the table is intended to be the
        package object's package_id field.
    """

    def __init__(self, size=10):
        self.size = size
        self.table = [None for _ in range(self.size)]


    def _hashing_method(self, package_id):
        """Hashing method is simply the package_id mod 10."""
        return package_id % 10


    def insert(self, package_obj):
        """This function inserts a package object into the hash table."""
        if package_obj is None:
            raise TypeError("Error encountered, user attempted to insert None into the hash table.")
        
        else:
            hash_key = self._hashing_method(package_obj.package_id)
            if self.table[hash_key] is None:
                self.table[hash_key] = [package_obj]

            else:
                self.table[hash_key].append(package_obj)


    def lookup(self, target_package_id):
        """
            This function takes a target package_id and returns a package object from the
            the hash table if there exists a package object in the hash table with a
            matching package_id value. Otherwise, it will return None.
        """
        lookup_hash = self._hashing_method(target_package_id)
        lookup_packages = self.table[lookup_hash]
        
        if lookup_packages is None:
            return None
        
        else:
            for package in lookup_packages:
                if package.package_id == target_package_id:
                    return package

            # We should never get down here.
            # If we do, that indicates some type of implementation exception.
            raise Exception(f"Exception encountered, unable to return a package object associated with {target_package_id=}.\n")
           

    def __str__(self):
        return "\n".join([
            f"{self.size=}",
            f"{self.table=}"
        ])


    def __repr__(self):
        return "\n".join([
            f"{self.size=}",
            f"{self.table=}"
        ])