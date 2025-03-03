class Admin:  #Admin Class
    def __init__(self, adminID, name, email):
        self.adminID = adminID
        self.name = name
        self.email = email

    def assignDeliveryTask(self):
        pass  #Logic to assign a delivery task

    def checkDeliveryStatus(self):
        pass  #Logic to check delivery status

    #Getters and Setters for admin
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
