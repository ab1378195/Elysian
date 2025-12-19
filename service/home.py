from utils.ocr import OCR
from service.recordService import RecordService
from service.configurationService import ConfigurationService
from time import strftime, sleep
from pyautogui import click, moveTo, mouseDown, mouseUp, dragRel, press, size
from utils.imageFinder import ImageFinder
import os


class Home:
    def __init__(self, log_queue):
        """实现家园日常任务的类

        Args:
            log_queue (Queue): 和procedure通信的队列
        """
        self.ocr = OCR()
        self.imgF = ImageFinder()
        self.log_queue = log_queue
        self.recordService = RecordService()
        self.record = self.recordService.get_home_record()
        configurationService = ConfigurationService()
        self.configuration = configurationService.get_home_configuration()
        self.current_day = strftime("%Y-%m-%d")
        self.resource_path = os.path.join("resources", "home")
        self.common_resource_path = os.path.join("resources", "common")
        # 由于包含三个可能的子任务，此变量用于标识当前游戏界面位置以优化任务间衔接，False代表在主界面，True代表在家园界面
        self.state = False

    def run(self):
        """执行家园日常任务"""
        self.log_queue.put(["开始执行家园日常任务", "INF2"])
        self.__run_reward()
        self.__run_quest()
        self.__run_storysweep()
        # 退回到主页面
        if self.state:
            press("esc")
            print(1)
        self.recordService.save_home_record(self.record)
        self.ocr.terminate()
        self.log_queue.put(["家园日常任务执行完成", "INF2"])
        self.log_queue.put(["exit", "INF1"])

    def __enter_home(self):
        """进入家园界面"""
        if self.state == False:
            self.ocr.click_text("家园", region_id=4)
            sleep(1)
            self.ocr.text("远征", region_id=4)
            sleep(0.5)
            # 可能遇到家园等级提升的通知
            if self.ocr.text("确定", region_id=7, blocking=0):
                click()
            sleep(0.5)

    def __run_reward(self):
        """执行领取家园体力和金币的任务"""

        def run_reward_validate():
            """检测是否需要执行家园奖励领取的任务

            Returns:
                boolean: True代表需要执行
            """
            if self.configuration["reward"] == "每日一次":
                record = self.recordService.get_home_record()
                if record and record["reward"] == self.current_day:
                    self.log_queue.put(["检测到今日已执行，任务自动取消", "INF1"])
                    return False
            return True

        self.log_queue.put(["开始执行家园金币和体力领取任务", "INF2"])
        if run_reward_validate():
            self.__enter_home()
            # 领取体力(这两个地方的领取要求鼠标点击操作的按下和抬起有一定延时，否则无法触发)
            if self.imgF.single(
                os.path.join(self.resource_path, "energy.png"), region_id=8
            ):
                moveTo(self.imgF.position)
                sleep(0.5)
                mouseDown()
                sleep(0.2)
                mouseUp()
                sleep(1)
                self.ocr.click_text("取出体力", region_id=4)
                # 如果领取的体力超过上限，这里已经退至家园界面，并有黑条幅的通知
                sleep(1)
                click()
                sleep(1)
                # 如果领取的体力未超上限，领取框还需手动关闭
                if self.imgF.single(
                    os.path.join(self.common_resource_path, "close.png"), region_id=2
                ):
                    moveTo(self.imgF.position)
                    sleep(0.2)
                    click()
                    sleep(1)
                self.log_queue.put(["体力已领取", "INF1"])
            else:
                self.log_queue.put(["未识别到体力领取点", "ERR"])
            # 退回主页面重进，否则直接点击领取金币无效(暂未清楚原因)
            sleep(1)
            press("esc")
            sleep(1)
            self.__enter_home()
            # 领取金币
            if self.imgF.single(
                os.path.join(self.resource_path, "coin.png"), region_id=8
            ):
                moveTo(self.imgF.position)
                sleep(0.5)
                mouseDown()
                sleep(0.2)
                mouseUp()
                sleep(1)
                click()
                self.log_queue.put(["金币已领取", "INF1"])
            else:
                self.log_queue.put(["未识别到金币领取点", "ERR"])
            self.record["reward"] = self.current_day
            self.state = True
        self.log_queue.put(["家园金币和体力领取任务执行完成", "INF2"])
        sleep(1)

    def __run_quest(self):
        """执行家园打工任务"""

        def run_quest_validate():
            """检测是否需要执行家园打工的任务

            Returns:
                boolean: True代表需要执行
            """
            if self.configuration["quest"] == "每日一次":
                record = self.recordService.get_home_record()
                if record and record["quest"] == self.current_day:
                    self.log_queue.put(["检测到今日已执行，任务自动取消", "INF1"])
                    return False
            return True

        self.log_queue.put(["开始执行家园打工任务", "INF2"])
        if run_quest_validate():
            self.__enter_home()
            self.ocr.click_text("打工", region_id=4)
            sleep(1)
            self.ocr.click_text("领取奖励", region_id=4)
            sleep(3)
            # 无奖励可领取则不会有确定窗口弹出
            if self.ocr.click_text("确定", region_id=7, blocking=0):
                self.log_queue.put(["打工奖励已领取", "INF1"])
            else:
                self.log_queue.put(["无打工奖励领取", "INF1"])
            sleep(1)
            self.ocr.click_text("一键打工", region_id=4)
            sleep(1)
            self.ocr.click_text("一键打工", region_id=7)
            sleep(1)
            click()
            sleep(1)
            # 如果无法进行打工，点击后窗口不会关闭，需要点击取消
            if self.ocr.click_text("取消", region_id=7, blocking=0):
                self.log_queue.put(["无法进行打工", "WAR"])
            else:
                self.log_queue.put(["已指派打工任务", "INF1"])
            sleep(1)
            press("esc")
            self.state = True
            self.record["quest"] = self.current_day
        self.log_queue.put(["家园打工任务执行完成", "INF2"])
        sleep(1)

    def __run_storysweep(self):
        """执行家园远征任务"""

        def run_storysweep_validate():
            """检测是否需要执行家园远征任务

            Returns:
                boolean: True代表需要执行
            """
            if self.configuration["storysweep"][0] == "每日一次":
                record = self.recordService.get_home_record()
                if record and record["storysweep"] == self.current_day:
                    self.log_queue.put(["检测到今日已执行，任务自动取消", "INF1"])
                    return False
            return True

        self.log_queue.put(["开始执行家园远征任务", "INF2"])
        if run_storysweep_validate():
            self.__enter_home()
            self.ocr.click_text("远征", region_id=4)
            sleep(3)
            # 不领取当日的远征奖励，避免次日任务无法完成
            if (
                "storysweep" in self.record
                and self.record["storysweep"] == self.current_day
            ):
                self.log_queue.put(["今日已领取家园远征奖励，不再尝试领取", "INF1"])
            else:
                if self.ocr.click_text("完成远征", blocking=0):
                    sleep(1)
                    self.ocr.click_text("确定", region_id=7)
                    sleep(1)
                    self.log_queue.put(["家园远征奖励已领取", "INF1"])
                else:
                    self.log_queue.put(["无可领取的家园远征奖励", "INF1"])
            # 仅远征黑核
            self.ocr.click_text("材料")
            sleep(2)
            WIDTH, HEIGHT = size()
            X_CENTER = WIDTH >> 1
            Y_CENTER = HEIGHT >> 1
            # 先翻页至上边
            while True:
                if self.ocr.find("最近") is None and self.ocr.find("完成") is None:
                    moveTo(X_CENTER, Y_CENTER)
                    dragRel(0, 200, duration=1)
                    sleep(1)
                else:
                    break
            sleep(2)
            # 执行远征派遣
            i = 0
            MAX_TIMES = int(self.configuration["storysweep"][1])
            while True:
                # 若开始远征按钮数目不够，向下滚动页面
                position_list = self.ocr.find_all("开始远征")
                if len(position_list) <= 2:
                    moveTo(X_CENTER, Y_CENTER)
                    dragRel(0, -200, duration=1)
                    sleep(1)
                    continue
                # 黑核的文本较难匹配，采用图片匹配
                while True:
                    if self.imgF.single(
                        os.path.join(self.resource_path, "Anti-Entropy.png"),
                        region_id=8,
                    ):
                        base_position = self.imgF.position  # 图片坐标
                        break
                    sleep(0.5)
                # 寻找与图片对应的远征按钮
                min_y_distance = 2000
                for position in position_list:
                    # 排除纵坐标小于图片纵坐标的按钮
                    if position[1] < base_position[1]:
                        continue
                    # 选择纵坐标最近的按钮
                    if min_y_distance > position[1] - base_position[1]:
                        min_y_distance = position[1] - base_position[1]
                        min_y_position = position
                moveTo(min_y_position)
                sleep(0.2)
                click()
                sleep(0.5)
                self.ocr.click_text("一键", region_id=4)
                sleep(1)
                self.ocr.click_text("确定", region_id=4)
                sleep(2)
                # 体力耗尽，退出
                if self.ocr.text("体力", region_id=6, blocking=0):
                    self.log_queue.put(["体力已用尽", "INF1"])
                    self.imgF.single(
                        os.path.join(self.common_resource_path, "close.png"),
                        region_id=2,
                    )
                    moveTo(self.imgF.position)
                    sleep(0.2)
                    click()
                    sleep(1)
                    break
                # 远征次数用尽，退出
                if self.ocr.text("确定", region_id=4, blocking=0):
                    self.log_queue.put(["已达最大远征次数", "INF1"])
                    break
                i += 1
                # 若到达配置次数，退出
                if i == MAX_TIMES:
                    self.log_queue.put(["已达到配置的远征次数", "INF1"])
                    break
            # 该任务为三个子任务中最后一个，如果执行完成了直接退回游戏主界面
            press("home")
            self.state = False
            self.record["storysweep"] = self.current_day
        self.log_queue.put(["家园远征任务执行完成", "INF2"])
        sleep(1)
