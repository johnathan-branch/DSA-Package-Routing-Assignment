class Package:
    """"A package object is intended to contain the data 
        that is read in from the package CSV file and has the following fields:

        Package ID (integer), 
        Address (string),
        City (string),
        State (string),
        Zip (string),
        Delivery Deadline (string),
        Weight KILO (float), 
        Special Notes (string)
    """
    
    def __init__(self, package_id, address, city, state, zip, delivery_deadline, weight_kilo, special_notes):

        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.weight_kilo = weight_kilo
        self.special_notes = special_notes    
        self.loading_time = 0.0 # making this a float for now, may change to datetime
        self.delivery_time = 0.0 # making this a float for now, may change to datetime


    def __str__(self):
        return "{" + "\n".join([
            f"{self.package_id=}",
            f"{self.address=}",
            f"{self.city=}",
            f"{self.state=}",
            f"{self.zip=}",
            f"{self.delivery_deadline=}",
            f"{self.weight_kilo=}",
            f"{self.special_notes=}",
            f"{self.loading_time=}",
            f"{self.delivery_time=}",
        ]) + "}"
    

    def __repr__(self):
        return "{" + "\n".join([
            f"{self.package_id=}",
            f"{self.address=}",
            f"{self.city=}",
            f"{self.state=}",
            f"{self.zip=}",
            f"{self.delivery_deadline=}",
            f"{self.weight_kilo=}",
            f"{self.special_notes=}",
            f"{self.loading_time=}",
            f"{self.delivery_time=}",
        ]) + "}"