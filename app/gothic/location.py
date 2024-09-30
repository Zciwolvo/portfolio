import uuid

class Location:
    def __init__(self, image_path, image_location_X, image_location_Y, map):
        self.image_path = image_path
        self.image_location_X = image_location_X
        self.image_location_Y = image_location_Y
        self.map = map
        self.location_id = str(uuid.uuid4)
