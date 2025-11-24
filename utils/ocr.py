from api.PPOCR.PPOCR_api import GetOcrApi
from pyautogui import screenshot, moveTo, click, size
from time import sleep
from io import BytesIO


class OCR:
    """the OCR class to find text position on the screen, based on PPOCR api (only support Chinese)"""

    def __init__(self):
        """basic attributes"""
        argument = {"config_path": "models/config_chinese.txt"}
        self.ocr = GetOcrApi(
            exePath="resources\\PaddleOCR-json_v1.4.1\\PaddleOCR-json.exe",
            argument=argument,
        )
        width, height = size()
        self.width_half = width >> 1
        self.height_half = height >> 1
        self.point_list = [
            (0, 0),  # full-screen point
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

    def find(self, text, region_id=0, match=0):
        """find the text position on the screen

        Args:
            text (String): the text needs to be found
            match (int, optional): the matching type, 1 means strict matching, 0 means the text is included in any other texts. Defaults to 0.

        Returns:
            List: the position of the text, return None if not found
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
        """move mouse to the targeted text in the screen

        Args:
            text (String): the text needs to be found
            blocking (int, optional): the blocking type, 1 means keeping searching until found it, 0 means only found once. Defaults to 1.
            match (int, optional): the matching type, 1 means strict matching, 0 means the text is included in any other texts. Defaults to 0.

        Returns:
            boolean: find the text or not
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
        """move mouse to the targeted text in the screen and click

        Args:
            text (String): the text needs to be found
            blocking (int, optional): the blocking type, 1 means keeping searching until found it, 0 means only found once. Defaults to 1.
            match (int, optional): the matching type, 1 means strict matching, 0 means the text is included in any other texts. Defaults to 0.

        Returns:
            boolean: find the text or not
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
        """terminate the ocr thread"""
        self.ocr.exit()
