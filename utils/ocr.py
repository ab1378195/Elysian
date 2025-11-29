from api.PPOCR.PPOCR_api import GetOcrApi
from pyautogui import screenshot, moveTo, click, size
from time import sleep
from io import BytesIO


class OCR:
    def __init__(self):
        """在屏幕中匹配文本的类"""
        argument = {"config_path": "models/config_chinese.txt"}
        self.ocr = GetOcrApi(
            exePath="resources\\PaddleOCR-json_v1.4.1\\PaddleOCR-json.exe",
            argument=argument,
        )
        width, height = size()
        self.width_half = width >> 1
        self.height_half = height >> 1
        self.point_list = [
            (0, 0),  # 全屏的原点
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

    def find(self, text, region_id=0, match=0):
        """在屏幕中找到首个匹配的文本的位置，如果没匹配到返回None

        Args:
            text (String): 要匹配的文本
            region_id (int, optional): 区域编号. Defaults to 0.
            match (int, optional): 匹配模式，1为严格匹配要求识别到的文本完全对应，0为模糊匹配，包含目标文本即可. Defaults to 0.

        Returns:
            List: 目标文本中心点的横纵坐标
        """
        if region_id == 0:
            image = screenshot()
        else:
            image = screenshot(
                region=(
                    self.point_list[region_id][0],
                    self.point_list[region_id][1],
                    self.width_half,
                    self.height_half,
                )
            )
        image_byte_arr = BytesIO()
        image.save(image_byte_arr, format="JPEG", quality=85)
        image_bytes = image_byte_arr.getvalue()
        res = self.ocr.runBytes(image_bytes)
        for data in res["data"]:
            if match == 0 and text in data["text"]:
                return [
                    ((data["box"][0][0] + data["box"][2][0]) >> 1)
                    + self.point_list[region_id][0],
                    ((data["box"][0][1] + data["box"][2][1]) >> 1)
                    + self.point_list[region_id][1],
                ]
            elif match == 1 and text == data["text"]:
                return [
                    ((data["box"][0][0] + data["box"][2][0]) >> 1)
                    + self.point_list[region_id][0],
                    ((data["box"][0][1] + data["box"][2][1]) >> 1)
                    + self.point_list[region_id][1],
                ]
        return None

    def text(self, text, blocking=1, region_id=0, match=0):
        """将鼠标移到目标文本的中心点，匹配到了返回True

        Args:
            text (String): 目标文本
            blocking (int, optional): 阻塞模式，1代表一直寻找直到匹配到，0代表只进行一次匹配. Defaults to 1.
            region_id (int, optional): 区域编号. Defaults to 0.
            match (int, optional): 匹配模式，1为严格匹配要求识别到的文本完全对应，0为模糊匹配，包含目标文本即可. Defaults to 0.

        Returns:
            boolean: 匹配到了返回True
        """
        while True:
            position = self.find(text, region_id, match)
            if position is not None:
                moveTo(position)
                sleep(0.2)
                return True
            elif blocking == 0:
                return False

    def click_text(self, text, blocking=1, region_id=0, match=0):
        """将鼠标移到目标文本中心点并点击一次，匹配到了返回True

        Args:
            text (String): 目标文本
            blocking (int, optional): 阻塞模式，1代表一直寻找直到匹配到，0代表只进行一次匹配. Defaults to 1.
            region_id (int, optional): 区域编号. Defaults to 0.
            match (int, optional): 匹配模式，1为严格匹配要求识别到的文本完全对应，0为模糊匹配，包含目标文本即可. Defaults to 0.

        Returns:
            boolean: 匹配到了返回True
        """
        while True:
            position = self.find(text, region_id, match)
            if position is not None:
                moveTo(position)
                sleep(0.2)
                click()
                return True
            elif blocking == 0:
                return False

    def terminate(self):
        """终止OCR线程"""
        self.ocr.exit()
