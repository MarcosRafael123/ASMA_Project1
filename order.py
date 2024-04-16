class Order:
    def __init__(self, id=None, center=None, destination=(0.0,0.0), weight=0):
        self._id = id
        self._center = center
        self._destination = destination  # (latitude, longitude)
        self._weight = weight

    # Getter and setter for id attribute
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    # Getter and setter for weight attribute
    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    # Getter and setter for destination attribute
    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    # Getter and setter for center attribute
    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value

    def __str__(self):
        return f"Order ID={self._id} center={self._center} weight={self._weight} dest={self._destination}"
    
    def to_dict(self):
        return {
            "order_id": self._id,
            "center": self._center,
            "destination": self._destination,
            "weight": self._weight
        }