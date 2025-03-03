from datetime import date


class System:  # System Class
    def authenticateUser(self):
        # Authenticate user credentials
        pass  # Functionality to verify user authentication

    def processPayment(self):
        # Functionality to handle payment processing
        pass


class Admin:  # Admin Class
    def __init__(self, adminID, name, email):
        self.adminID = adminID
        self.name = name
        self.email = email

    def assignDeliveryTask(self):
        pass  # Logic to assign a delivery task

    def checkDeliveryStatus(self):
        pass  # Logic to check delivery status

    # Getters and Setters for admin
    def getAdminID(self):
        return self.adminID

    def setAdminID(self, adminID):
        self.adminID = adminID

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        self.email = email


class DeliveryStaff:  # DeliveryStaff Class
    def __init__(self, staffID, name, phone):
        self.staffID = staffID
        self.name = name
        self.phone = phone

    def updateDeliveryStatus(self):
        pass  # Logic to update delivery status

    # getters and setters for staff
    def getStaffID(self):
        return self.staffID

    def setStaffID(self, staffID):
        self.staffID = staffID

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getPhone(self):
        return self.phone

    def setPhone(self, phone):
        self.phone = phone


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
# Object Creation and Delivery Note Generation

# Creating a System object
system = System()
# Creating an Admin object
admin = Admin(1, "Mansoor", "mansoor@example.com")
# Creating a Delivery Staff object
staff = DeliveryStaff(101, "Ali", "555-1234")
# Creating a Customer object
customer = Customer(101, "Sarah Johnson", "sarah.johnson@example.com", "1234567890", "45 Knowledge Avenue, Dubai, UAE")
# Creating a Delivery object
delivery = Delivery(5001, customer, "In Progress", date.today(), customer.getAddress())
# Generating the Delivery Note
delivery.generateDeliveryNote()
