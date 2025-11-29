from pyautogui import locateAllOnScreen, locateCenterOnScreen, size


class ImageFinder:
    def __init__(self):
        """在屏幕中匹配图片的类"""
        self.position = []
        width, height = size()
        self.width_half = width >> 1
        self.height_half = height >> 1
        self.point_list = [
            (-1, -1),  # 无用点，用于占据一个索引方便后续索引匹配
            (0, 0),  # 左上角区域的原点
            (self.width_half, 0),  # 右上角区域的原点
            (0, self.height_half),  # 左下角区域的原点
            (self.width_half, self.height_half),  # 右下角区域的原点
            (self.width_half >> 1, self.height_half >> 1),  # 中间区域的原点
            (self.width_half >> 1, 0),  # 顶部区域的原点
            (self.width_half >> 1, self.height_half),  # 底部区域的原点
            (0, self.height_half >> 1),  # 左侧区域的原点
            (self.width_half, self.height_half >> 1),  # 右侧区域的原点
        ]

    def single(self, image, confidence=0.8, region_id=0):
        """找到屏幕中首个匹配图片的位置，如果找到，将坐标存于self.position中

        Args:
            image (String): 要匹配的图片的路径
            confidence (float, optional): 置信度. Defaults to 0.8.
            region_id (int, optional): 匹配区域编号. Defaults to 0.

        Returns:
            boolean: 找到返回True
        """
        self.position.clear()
        try:
            if region_id == 0:
                res = locateCenterOnScreen(image, confidence=confidence)
            else:
                res = locateCenterOnScreen(
                    image,
                    confidence=confidence,
                    region=(
                        self.point_list[region_id][0],
                        self.point_list[region_id][1],
                        self.width_half,
                        self.height_half,
                    ),
                )
            self.position = [float(res[0]), float(res[1])]
            return True
        except:
            return False

    def all(self, image, confidence=0.8):
        """找到屏幕中所有匹配的图片，若找到，将坐标存在self.position中

        Args:
            image (String): 要匹配图片的路径
            confidence (float, optional): 置信度. Defaults to 0.8.

        Returns:
            boolean: 找到返回True
        """
        self.position.clear()
        try:
            res = locateAllOnScreen(image, confidence=confidence)
            for point in res:
                self.position.append([float(point[0]), float(point[1])])
            return True
        except:
            return False
