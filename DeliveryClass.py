class Delivery:  # Delivery Class
    def __init__(self, deliveryID, customer, deliveryStatus, deliveryDate, deliveryAddress):
        self.deliveryID = deliveryID
        self.customer = customer
        self.deliveryStatus = deliveryStatus
        self.deliveryDate = deliveryDate
        self.deliveryAddress = deliveryAddress

    def updateStatus(self):
        pass  # Logic for updating the delivery status

    def generateDeliveryNote(self):
        """Generate and display the delivery note"""
        print("\n--- Delivery Note ---")
        print(f"Delivery ID: {self.deliveryID}")
        print(f"Customer Name: {self.customer.getName()}")
        print(f"Delivery Address: {self.deliveryAddress}")
        print(f"Delivery Date: {self.deliveryDate}")
        print(f"Delivery Status: {self.deliveryStatus}")
        print("----------------------")

        # getters and setters for delivery class

    def getDeliveryID(self):
        return self.deliveryID

    def setDeliveryID(self, deliveryID):
        self.deliveryID = deliveryID

    def getCustomer(self):
        return self.customer

    def setCustomer(self, customer):
        self.customer = customer

    def getDeliveryStatus(self):
        return self.deliveryStatus

    def setDeliveryStatus(self, deliveryStatus):
        self.deliveryStatus = deliveryStatus

    def getDeliveryDate(self):
        return self.deliveryDate

    def setDeliveryDate(self, deliveryDate):
        self.deliveryDate = deliveryDate

    def getDeliveryAddress(self):
        return self.deliveryAddress

    def setDeliveryAddress(self, deliveryAddress):
        self.deliveryAddress = deliveryAddress
