from pyautogui import size, locate, locateAll, locateCenterOnScreen
from utils.screenshot import Screenshot


class ImageFinder:
    def __init__(self):
        """在崩坏3窗口中匹配图片的类，需要崩坏3窗口已存在，single中可特别截取电脑屏幕"""
        self.position = []
        width, height = size()
        width_half = width >> 1
        height_half = height >> 1
        self.point_list = [
            (0, 0, width, height),  # 全屏
            (0, 0, width_half, height_half),  # 左上角区域
            (width_half, 0, width, height_half),  # 右上角区域
            (0, height_half, width_half, height),  # 左下角区域
            (width_half, height_half, width, height),  # 右下角区域
            (
                width_half >> 1,
                height_half >> 1,
                (width_half + width) >> 1,
                (height_half + height) >> 1,
            ),  # 中间区域
            (
                width_half >> 1,
                0,
                (width_half + width) >> 1,
                height_half,
            ),  # 顶部区域
            (
                width_half >> 1,
                height_half,
                (width_half + width) >> 1,
                height,
            ),  # 底部区域
            (
                0,
                height_half >> 1,
                width_half,
                (height_half + height) >> 1,
            ),  # 左侧区域
            (
                width_half,
                height_half >> 1,
                width,
                (height_half + height) >> 1,
            ),  # 右侧区域
        ]
        self.screenshot = Screenshot()

    def single(self, image, confidence=0.8, region_id=0):
        """找到崩坏3截图中首个匹配图片的位置，如果找到，将坐标存于self.position中。

        Args:
            image (String): 要匹配的图片的路径
            confidence (float, optional): 置信度. Defaults to 0.8.
            region_id (int, optional): 匹配区域编号，如果为-1会截取电脑屏幕匹配. Defaults to 0.

        Returns:
            boolean: 找到返回True
        """
        self.position.clear()
        try:
            if region_id == -1:
                res = locateCenterOnScreen(image, confidence=confidence)
                region_id = 0  # 修改为全屏区域编号以对应后续的坐标修正操作
            else:
                window_image = self.screenshot.screenshot()
                if region_id != 0:
                    window_image = window_image.crop(self.point_list[region_id])
                res = locate(image, window_image, confidence=confidence)
            self.position = [
                float(res[0]) + self.point_list[region_id][0],
                float(res[1]) + self.point_list[region_id][1],
            ]
            return True
        except:
            return False

    def all(self, image, confidence=0.8):
        """找到崩坏3截图中所有匹配的图片，若找到，将坐标存在self.position中

        Args:
            image (String): 要匹配图片的路径
            confidence (float, optional): 置信度. Defaults to 0.8.

        Returns:
            boolean: 找到返回True
        """
        self.position.clear()
        try:
            window_image = self.screenshot.screenshot()
            res = locateAll(image, window_image, confidence=confidence)
            for point in res:
                self.position.append([float(point[0]), float(point[1])])
            return True
        except:
            return False
