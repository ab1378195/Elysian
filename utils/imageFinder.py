from pyautogui import locateAllOnScreen, locateCenterOnScreen, size


class ImageFinder:
    """the class to find image position on the screen, based on pyautogui lib"""

    def __init__(self):
        """basic attributes"""
        self.position = []
        width, height = size()
        self.width_half = width >> 1
        self.height_half = height >> 1
        self.point_list = [
            (-1, -1), # useless point, just occupy the zero index and never be used
            (0, 0),  # left-top region
            (self.width_half, 0),  # right-top region
            (0, self.height_half),  # left-bottom region
            (self.width_half, self.height_half),  # right-bottom region
            (self.width_half >> 1, self.height_half >> 1),  # middle region
            (self.width_half >> 1, 0),  # top region
            (self.width_half >> 1, self.height_half),  # bottom region
            (0, self.height_half >> 1),  # left region
            (self.width_half, self.height_half >> 1),  # right region
        ]

    def single(self, image, confidence=0.8, region_id=0):
        """find the first matched image on the screen. If found, the position is stored in self.position

        Args:
            image (String): the file path of the image needs to be found
            confidence (float, optional): minimum level of image matching. Defaults to 0.8.

        Returns:
            boolean: find image on the screen or not
        """
        self.position.clear()
        try:
            if region_id == 0:
                res = locateCenterOnScreen(image, confidence=confidence)
            else:
                res = locateCenterOnScreen(image, confidence=confidence, region=(
                    self.point_list[region_id][0],
                    self.point_list[region_id][1],
                    self.width_half,
                    self.height_half,
                ))
            self.position = [float(res[0]), float(res[1])]
            return True
        except:
            return False

    def all(self, image, confidence=0.8):
        """find all matched images on the screen, the matching positions will be stored in self.position

        Args:
            image (String): the file path of the image needs to be found
            confidence (float, optional): the minimum level of image matching. Defaults to 0.8.

        Returns:
            boolean: find matching images or not
        """
        self.position.clear()
        try:
            res = locateAllOnScreen(image, confidence=confidence)
            for point in res:
                self.position.append([float(point[0]), float(point[1])])
            return True
        except:
            return False
