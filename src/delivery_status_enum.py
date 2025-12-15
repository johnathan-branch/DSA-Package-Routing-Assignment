from enum import Enum

class DeliveryStatus(Enum):
    AT_HUB = "at the hub"
    EN_ROUTE = "en route"
    DELIVERED = "delivered"
    DELAYED = "DELAYED"
    NOT_DELIVERED = "not delivered yet"