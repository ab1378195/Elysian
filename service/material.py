from utils.ocr import OCR
from time import sleep
from service.recordService import RecordService
from service.configurationService import ConfigurationService
from time import strftime
from pyautogui import click, press


class Material:
    def __init__(self, log_queue):
        self.ocr = OCR()
        self.log_queue = log_queue
        self.recordService = RecordService()
        self.configurationService = ConfigurationService()
        self.current_day = strftime("%Y-%m-%d")

    def run(self):
        def run_validate():
            """检测是否需要执行材料活动任务

            Returns:
                boolean: True代表需要执行
            """
            if (
                self.configurationService.get_material_configuration()["frequency"]
                == "每日一次"
            ):
                record = self.recordService.get_material_record()
                if record and record["time"] == self.current_day:
                    self.log_queue.put(
                        ["检测到今日已执行过该任务，任务自动取消", "INF1"]
                    )
                    return False
            return True

        self.log_queue.put(["开始执行材料活动任务", "INF2"])
        if run_validate():
            # 执行任务部分
            self.ocr.click_text("出击", region_id=9)
            sleep(3)
            self.ocr.click_text("出击", region_id=6)
            sleep(1)
            self.ocr.click_text("材料远征", region_id=7)
            sleep(3)
            if self.ocr.text("一键减负", region_id=4, blocking=0):
                self.log_queue.put(["检测到一键减负按钮", "INF1"])
                click()
                sleep(2)
                if self.ocr.click_text("减负", region_id=7, blocking=0):
                    sleep(1)
                    self.ocr.click_text("确定", region_id=7)
                else:
                    # 可能当日减负次数已达上限
                    self.log_queue.put(["未检测到减负按钮", "WAR"])
                sleep(2)
            else:
                # 可能已无法减负
                self.log_queue.put(["未检测到一键减负按钮", "WAR"])
            press("home")
        self.recordService.save_material_record({"time": self.current_day})
        self.log_queue.put(["材料活动任务执行完成", "INF2"])
        self.log_queue.put(["exit", "INF1"])
