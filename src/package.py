from delivery_status_enum import DeliveryStatus

class Package:
    """"A package object is intended to contain the data 
        that is read in from the package CSV file that has the following fields:

        Package ID (integer), 
        Address (string),
        City (string),
        State (string),
        Zip (string),
        Delivery Deadline (string),
        Weight KILO (float), 
        Special Notes (string)

        A package also contains the fields delivery_status and delivery_time.
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
        self.delivery_status = DeliveryStatus.AT_HUB
        self.delivery_time = None


    def __str__(self):
        return "\n".join([
            f"{self.package_id=}",
            f"{self.address=}",
            f"{self.city=}",
            f"{self.state=}",
            f"{self.zip=}",
            f"{self.delivery_deadline=}",
            f"{self.weight_kilo=}",
            f"{self.special_notes=}",
            f"{self.delivery_status.value=}",
            f"{self.delivery_time=}"
        ])+"\n"
    

    def __repr__(self):
        return "\n".join([
            f"{self.package_id=}",
            f"{self.address=}",
            f"{self.city=}",
            f"{self.state=}",
            f"{self.zip=}",
            f"{self.delivery_deadline=}",
            f"{self.weight_kilo=}",
            f"{self.special_notes=}",
            f"{self.delivery_status.value=}",
            f"{self.delivery_time=}"
        ])+"\n"