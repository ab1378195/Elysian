from api.PPOCR.PPOCR_api import GetOcrApi
from pyautogui import moveTo, click, size, screenshot
from time import sleep
from io import BytesIO
from utils.screenshot import Screenshot


class OCR:
    def __init__(self):
        """在崩坏3屏幕中匹配文本的类，region_id=-1会截取电脑屏幕"""
        argument = {"config_path": "models/config_chinese.txt"}
        self.ocr = GetOcrApi(
            exePath="resources\\PaddleOCR-json_v1.4.1\\PaddleOCR-json.exe",
            argument=argument,
        )
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

    def find(self, text, region_id=0, match=0):
        """在屏幕中找到首个匹配的文本的位置，如果没匹配到返回None

        Args:
            text (String): 要匹配的文本
            region_id (int, optional): 区域编号，-1会截取电脑屏幕. Defaults to 0.
            match (int, optional): 匹配模式，1为严格匹配要求识别到的文本完全对应，0为模糊匹配，包含目标文本即可. Defaults to 0.

        Returns:
            List: 目标文本中心点的横纵坐标
        """
        if region_id == -1:
            image = screenshot()
            region_id = 0  # 修改为全屏区域编号以对应后续的坐标修正操作
        else:
            image = self.screenshot.screenshot()
            if region_id != 0:
                image = image.crop(self.point_list[region_id])
        image_byte_arr = BytesIO()
        image.save(image_byte_arr, format="JPEG", quality=85)
        image_bytes = image_byte_arr.getvalue()
        res = self.ocr.runBytes(image_bytes)
        for data in res["data"]:
            # 未检测到任何文本
            if type(data) == str:
                continue
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

    def find_all(self, text):
        """全屏查找所有包含指定文本的位置，返回包含所有坐标的一个列表

        Args:
            text (String): 要匹配的文本

        Returns:
            List: 所有匹配点坐标的列表，未找到返回[ ]
        """
        image = self.screenshot.screenshot()
        image_byte_arr = BytesIO()
        image.save(image_byte_arr, format="JPEG", quality=85)
        image_bytes = image_byte_arr.getvalue()
        res = self.ocr.runBytes(image_bytes)
        position = []
        for data in res["data"]:
            # 未检测到任何文本
            if type(data) == str:
                continue
            if text in data["text"]:
                position.append(
                    [
                        ((data["box"][0][0] + data["box"][2][0]) >> 1)
                        + self.point_list[0][0],
                        ((data["box"][0][1] + data["box"][2][1]) >> 1)
                        + self.point_list[0][1],
                    ]
                )
        return position

    def text(self, text, blocking=1, region_id=0, match=0):
        """将鼠标移到目标文本的中心点，匹配到了返回True

        Args:
            text (String): 目标文本
            blocking (int, optional): 阻塞模式，1代表一直寻找直到匹配到，0代表只进行一次匹配. Defaults to 1.
            region_id (int, optional): 区域编号，-1会截取电脑屏幕. Defaults to 0.
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
            region_id (int, optional): 区域编号，-1会截取电脑屏幕. Defaults to 0.
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
