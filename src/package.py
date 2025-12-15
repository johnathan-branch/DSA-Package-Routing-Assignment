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

        A package also contains the fields delivery_status, delivery_time, delivery_truck_no.
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
        self.delivery_truck_no = None


    def __str__(self):
        return ", ".join([
            f"package_id={self.package_id}",
            f"address={self.address}",
            f"city={self.city}",
            f"state={self.state}",
            f"zip={self.zip}",
            f"delivery_deadline={self.delivery_deadline}",
            f"weight={self.weight_kilo}",
            f"special_notes={self.special_notes}",
            f"delivery_status={self.delivery_status.value}",
            f"delivery_time={self.delivery_time}",
            f"delivery_truck_no={self.delivery_truck_no}"
        ])+"\n\n"
    

    def __repr__(self):
        return ", ".join([
            f"package_id={self.package_id}",
            f"address={self.address}",
            f"city={self.city}",
            f"state={self.state}",
            f"zip={self.zip}",
            f"delivery_deadline={self.delivery_deadline}",
            f"weight={self.weight_kilo}",
            f"special_notes={self.special_notes}",
            f"delivery_status={self.delivery_status.value}",
            f"delivery_time={self.delivery_time}",
            f"delivery_truck_no={self.delivery_truck_no}"
        ])+"\n\n"