from utils.ocr import OCR
from utils.imageFinder import ImageFinder
from pyautogui import click, moveRel, moveTo, press
from time import sleep
import os


class Activity:
    def __init__(self, log_queue, reward_flag):
        """领取活跃度奖励的类

        Args:
            log_queue (Queue): 与procedure通信的队列
            reward_flag (boolean): True代表需要领取历练值奖励
        """
        self.ocr = OCR()
        self.imgF = ImageFinder()
        self.log_queue = log_queue
        self.reward_flag = reward_flag
        self.resource_path = os.path.join("resources", "activity")
        self.common_resource_path = os.path.join("resources", "common")

    def run(self):
        """执行活跃度奖励领取"""
        self.log_queue.put(["开始执行活跃度奖励领取任务", "INF2"])
        self.ocr.text("任务", region_id=1)
        sleep(0.2)
        moveRel(-100, 0)
        sleep(0.2)
        click()
        sleep(1)
        # 点击作战任务(可能在历练任务等其它地方)
        while True:
            position_list = self.ocr.find_all("作战任务")
            # 在作战奖励或作战商店界面
            if len(position_list) == 1:
                moveTo(position_list[0])
                sleep(0.2)
                click()
                sleep(0.5)
                continue
            if len(position_list) >= 2:
                break
            sleep(0.5)
        target_position = position_list[0]
        for position in position_list[1:]:
            if position[1] > target_position[1]:
                target_position = position
        moveTo(target_position)
        sleep(0.2)
        click()
        sleep(1)
        self.ocr.click_text("一键领取", region_id=2)
        sleep(3)
        # 如果领取到了奖励，需要点击确定按钮关闭弹窗
        if self.ocr.click_text("确定", region_id=7, blocking=0):
            self.log_queue.put(["已领取任务奖励", "INF1"])
        else:
            self.log_queue.put(["无任务奖励可领取", "INF1"])
        sleep(3)
        # 如果需要领取历练值奖励且历练值奖励未被领取完才执行
        if self.reward_flag and self.ocr.find("明日", region_id=4) is None:
            while True:
                if self.imgF.all(
                    os.path.join(self.resource_path, "activity.png"), confidence=0.9
                ):
                    break
                sleep(0.5)
            # 只点击最右侧的活跃度奖励
            moveTo(self.imgF.position[-1])
            sleep(0.2)
            click()
            sleep(2)
            # 活跃度不足和活跃度奖励领取的窗口可统一关闭
            while True:
                if self.imgF.single(
                    os.path.join(self.common_resource_path, "close.png"), region_id=2
                ):
                    break
                sleep(0.5)
            moveTo(self.imgF.position)
            sleep(0.2)
            click()
            sleep(0.5)
        press("home")
        sleep(0.5)
        self.ocr.terminate()
        self.log_queue.put(["活跃度奖励领取任务执行完成", "INF2"])
        self.log_queue.put(["exit", "INF1"])
