class CustomMap:
    def __init__(
        self,
        name,
        image_path,
        w,
        h,
        initial_zoom,
    ):
        self.name = name
        self.image_path = image_path
        self.image_width = w
        self.image_height = h
        self.initial_zoom = initial_zoom

    def to_dict(self):
        return {
            "name": self.name,
            "image_path": self.image_path,
            "initial_zoom": self.initial_zoom,
        }
