class DeliveryStaff:  #DeliveryStaff Class
    def __init__(self, staffID, name, phone):
        self.staffID = staffID
        self.name = name
        self.phone = phone

    def updateDeliveryStatus(self):
        pass  #Logic to update delivery status

    #getters and setters for staff
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
