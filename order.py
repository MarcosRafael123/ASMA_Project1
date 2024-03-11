class Order:
    def __init__(self):
        self.id = None
        self.weight = None
        self.latitude = None
        self.longitude = None

    @property
    def id(self):
        return self.id

    @latitude.setter
    def id(self, value):
        self.id = value

    @property
    def weight(self):
        return self.weight

    @longitude.setter
    def weight(self, value):
        self.weight = value

    @property
    def latitude(self):
        return self.latitude

    @latitude.setter
    def latitude(self, value):
        self.latitude = value

    @property
    def longitude(self):
        return self.longitude

    @longitude.setter
    def longitude(self, value):
        self.longitude = value