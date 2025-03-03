class Customer:  # Customer Class
    def __init__(self, customerID, name, email, phone,
                 address):  # Parameterized constructor to initialize customer attirbutes
        self.customerID = customerID
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    def placeDelivery(self):
        pass  # Logic for placing a delivery request

    def trackDelivery(self):
        pass  # Logic to track delivery status

    # getters and setters for customer
    def getCustomerID(self):
        return self.customerID

    def setCustomerID(self, customerID):
        self.customerID = customerID

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        self.email = email

    def getPhone(self):
        return self.phone

    def setPhone(self, phone):
        self.phone = phone

    def getAddress(self):
        return self.address

    def setAddress(self, address):
        self.address = address
