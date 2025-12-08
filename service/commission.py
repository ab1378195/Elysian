from utils.ocr import OCR
from service.recordService import RecordService
from service.configurationService import ConfigurationService
from time import strftime, sleep
import os
from utils.imageFinder import ImageFinder
from pyautogui import click, moveRel, press


class Commission:
    def __init__(self, log_queue):
        """实现舰团委托的类

        Args:
            log_queue (Queue): 和procedure通信的队列
        """
        self.ocr = OCR()
        self.imgF = ImageFinder()
        self.log_queue = log_queue
        self.recordService = RecordService()
        configurationService = ConfigurationService()
        self.configuration = configurationService.get_commission_configuration()
        self.current_day = strftime("%Y-%m-%d")
        self.recource_path = os.path.join("resources", "commission")

    def run(self):
        """执行舰团委托"""

        def run_validate():
            """检测是否需要执行舰团委托任务

            Returns:
                boolean: True代表需要执行
            """
            if self.configuration["frequency"] == "每日一次":
                record = self.recordService.get_commission_record()
                if record and record["time"] == self.current_day:
                    self.log_queue.put(["检测到今日已执行，任务自动取消", "INF1"])
                    return False
            return True

        self.log_queue.put(["开始执行舰团委托任务", "INF2"])
        if run_validate():
            self.ocr.click_text("舰团", region_id=4)
            sleep(1)
            self.ocr.click_text("回收", region_id=3)
            sleep(1)
            self.ocr.text("奖池", region_id=2)
            # 如果有感叹号代表有奖励可领取
            if self.imgF.single(
                os.path.join(self.recource_path, "info.png"), region_id=2
            ):
                click()
                sleep(1)
                self.ocr.click_text("领取", region_id=4)
                sleep(1)
                self.ocr.click_text("确定", region_id=7)
                sleep(1)
                self.ocr.click_text("委托", region_id=2)
                sleep(1)
                self.log_queue.put(["舰团委托奖励已领取", "INF1"])
            else:
                self.log_queue.put(["无舰团委托奖励可领取", "INF1"])
            # 申请新委托
            self.ocr.click_text("申请", region_id=3)
            sleep(3)
            # 若已申请过新委托，点击后不会有新页面弹出
            if self.ocr.click_text("接受", region_id=2, blocking=0):
                sleep(1)
                click()  # 关闭干扰的黑色弹窗
                self.log_queue.put(["申请新委托", "INF1"])
            else:
                self.log_queue.put(["无新委托可申请", "INF1"])
            TIMES = int(self.configuration["times"])
            for i in range(TIMES):
                # 定位第一个委托的位置
                self.ocr.text("回收", region_id=1)
                sleep(0.2)
                moveRel(0, 100)
                sleep(0.2)
                click()
                sleep(2)
                # 材料不够需要购买
                if self.ocr.click_text("购买", region_id=4, blocking=0):
                    sleep(0.5)
                    click()
                    sleep(0.5)
                self.ocr.click_text("提交", region_id=4)
                sleep(0.5)
                self.ocr.click_text("提交委托", region_id=4)
                sleep(2)
                # 未弹出放入奖励弹窗，说明已达当日委托提交上限
                if self.ocr.click_text("放入", region_id=7, blocking=0):
                    sleep(0.5)
                    click()  # 关闭动画
                    sleep(1)
                    self.log_queue.put(["已提交{}个委托".format(i + 1), "INF1"])
                else:
                    sleep(0.5)
                    click()  # 关闭动画
                    sleep(2)
                    self.log_queue.put(["已达今日委托提交上限", "WAR"])
                    break
            self.log_queue.put(["共计提交了{}个委托".format(i), "INF1"])
            press("home")
        self.recordService.save_commission_record({"time": self.current_day})
        self.ocr.terminate()
        self.log_queue.put(["舰团委托任务执行完成", "INF2"])
        self.log_queue.put(["exit", "INF1"])
