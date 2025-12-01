import winreg
from subprocess import Popen
from pyautogui import click, moveTo, hotkey
import pygetwindow as gw
from utils.ocr import OCR
from time import sleep
from service.accountService import AccountService
from service.configurationService import ConfigurationService
from utils.imageFinder import ImageFinder
from math import pow
from pyperclip import copy
from api.mumu.mumu import Mumu
import psutil


class Launch:
    def __init__(self, log_queue):
        """启动崩坏3的类

        Args:
            log_queue (Queue): 与Procedure进行通信的队列
        """
        accountService = AccountService()
        self.account = accountService.get_login_account()
        if self.account.channel == "渠道服":
            configurationService = ConfigurationService()
            self.emulator_configuration = (
                configurationService.get_emulator_configuration()
            )
        self.logout = False
        self.log_queue = log_queue
        self.imgF = ImageFinder()
        self.ocr = OCR()

    def launch_game(self):
        """启动崩坏3"""
        windows = gw.getAllTitles()
        if "崩坏3" not in windows:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, "SOFTWARE\\miHoYo\\HYP\\1_1\\bh3_cn"
            ) as key:
                game_path, _ = winreg.QueryValueEx(key, "GameInstallPath")
            game_path += "\\BH3.exe"
            Popen([game_path])
            if self.account.channel == "渠道服":
                self.logout = True
            else:
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, "SOFTWARE\\miHoYo\\崩坏3"
                ) as key:
                    last_uid, _ = winreg.QueryValueEx(
                        key, "GENERAL_DATA_V2_LastLoginUserId_h47158221"
                    )
                if last_uid != int(self.account.uid):
                    self.logout = True
            sleep(10)
            self.enter_game()
        else:
            self.activate_game()
        self.ocr.terminate()
        self.log_queue.put(["启动成功", "INF2"])
        self.log_queue.put(["exit", "INF1"])

    def activate_game(self):
        """如果崩坏3存在，激活崩坏3为活跃窗口"""
        active_window = gw.getActiveWindow()
        if active_window.title != "崩坏3":
            game_window = gw.getWindowsWithTitle("崩坏3")
            # 崩坏3窗口已存在时才激活
            if game_window:
                game_window[0].activate()

    def enter_game(self):
        """进入崩坏3"""

        def login_verify():
            """验证是否已成功登录到舰桥页面"""
            sleep(10)
            self.ocr.text("当前模式", region_id=3)
            sleep(1)
            while True:
                flag_reward = False
                flag_abyss = False
                flag_announcement = False
                # 关闭游戏公告
                if self.ocr.text("空白", blocking=0, region_id=7):
                    sleep(0.5)
                    # 关闭活动公告
                    if self.imgF.single("resources//common//close.png", region_id=2):
                        moveTo(self.imgF.position)
                        sleep(0.2)
                        click()
                    # PV公告，只能点击空白区域关闭
                    else:
                        click()
                    sleep(2)
                else:
                    flag_announcement = True
                # 领取每日签到奖励和月卡奖励(采用严格匹配，因为可能匹配到未加入舰团时弹出的加入领取奖励)
                if self.ocr.click_text("领取", blocking=0, match=1, region_id=7):
                    sleep(2)
                    self.ocr.click_text("确定")
                    sleep(2)
                else:
                    flag_reward = True
                # 深渊结算
                if self.ocr.text("结算奖励", blocking=0):
                    sleep(2)
                    click()
                    sleep(2)
                else:
                    flag_abyss = True
                if flag_reward and flag_announcement and flag_abyss:
                    break

        def fill_login_box():
            """填写登录框的信息"""
            # 通过复制粘贴写入账号与密码信息
            self.ocr.click_text("账号密码", region_id=5)
            sleep(1)
            self.ocr.click_text("手机号", region_id=5)
            sleep(0.5)
            copy(self.account.account)
            hotkey("ctrl", "v")
            sleep(0.5)
            self.ocr.click_text("密码", region_id=5)
            sleep(0.5)
            copy(self.account.password)
            hotkey("ctrl", "v")
            sleep(0.5)
            self.ocr.click_text("进入游戏", region_id=5)
            # 同意用户协议
            while True:
                sleep(1)
                if self.ocr.click_text("同意", blocking=0, region_id=5, match=1):
                    sleep(10)
                if self.ocr.text("进入游戏", blocking=0, region_id=7):
                    sleep(3)
                    break
            # 选择登录渠道
            self.imgF.single("resources//login//channel.png", region_id=7)
            moveTo(self.imgF.position)
            sleep(0.2)
            click()
            sleep(1)
            if self.account.channel == "ios":
                # 由于OCR仅保留简中模型，英文识别效果不好，采用图片匹配
                self.imgF.single("resources//login//ios.png")
                moveTo(self.imgF.position)
                sleep(0.2)
                click()
            else:
                if self.account.channel == "官服":
                    self.account.channel = "全平台"
                if self.account.channel == "Android":
                    self.account.channel = "安卓"
                self.ocr.click_text(self.account.channel)
            sleep(1)
            self.ocr.click_text("确定")
            sleep(2)
            self.ocr.click_text("进入游戏", region_id=7)

        # 等待游戏加载完毕
        while True:
            self.activate_game()
            sleep(1)
            if self.ocr.text("进入游戏", 0, region_id=7):
                sleep(4)
                break
        # 执行登出操作
        if self.logout:
            if self.account.channel == "渠道服":
                self.log_queue.put(["检测到为渠道服账号，登出账号", "INF1"])
            else:
                self.log_queue.put(["检测到uid不符，登出账号", "INF1"])
            # 确认当前页面
            while True:
                if self.ocr.click_text("更换账号", 0, region_id=4):
                    sleep(1)
                    # 选择保留历史记录
                    self.ocr.text("保留", region_id=5)
                    base_position = self.ocr.find("保留", region_id=5)
                    self.imgF.single(
                        "resources//login//selected_radiobutton.png", region_id=5
                    )
                    distance = pow(self.imgF.position[0] - base_position[0], 2) + pow(
                        self.imgF.position[1] - base_position[1], 2
                    )
                    self.imgF.single(
                        "resources//login//unselected_radiobutton.png", region_id=5
                    )
                    # 若未选择的框离得更近，说明该框为保留历史记录的框，应当勾选
                    if (
                        pow(self.imgF.position[0] - base_position[0], 2)
                        + pow(self.imgF.position[1] - base_position[1], 2)
                        < distance
                    ):
                        moveTo(self.imgF.position)
                        click()
                    # 登出
                    sleep(1)
                    self.ocr.click_text("退出", region_id=5, match=1)
                    sleep(1)
                if self.ocr.click_text("登录其他账号", 0, 5) == 1:
                    sleep(1)
                    break
                if self.imgF.single("resources//login//QRcode.png"):
                    sleep(1)
                    break
            if self.account.channel == "渠道服":
                self.log_queue.put(["检测到为渠道服登录，启动模拟器", "INF1"])
                try:
                    mumu = Mumu(self.emulator_configuration["path"]).select(
                        self.emulator_configuration["index"]
                    )
                    mumu.power.start()
                    sleep(10)
                    mumu.window.show()
                    mumu.app.launch("com.github.haocen2004.bh3_login_simulation")
                except Exception as e:
                    self.log_queue.put([e, "ERR"])
                while True:
                    if self.imgF.single(
                        "resources//login//channel_ready1.png", region_id=9
                    ):
                        break
                    if self.imgF.single(
                        "resources//login//channel_ready2.png", region_id=9
                    ):
                        break
                    sleep(0.5)
                game_window = gw.getWindowsWithTitle("崩坏3")
                game_window[0].activate()
                while True:
                    sleep(0.5)
                    if self.imgF.single("resources//login//QRcode.png"):
                        break
                moveTo(self.imgF.position)
                sleep(0.2)
                click()
                sleep(0.2)
                mumu.window.show()
                self.ocr.click_text("扫描二维码")
                sleep(1)
                self.ocr.click_text("实时")
                sleep(0.5)
                game_window = gw.getWindowsWithTitle("崩坏3")
                game_window[0].activate()
                sleep(5)
                self.ocr.click_text("进入游戏", region_id=7)
                self.log_queue.put(["检测到登录成功，退出模拟器", "INF1"])
                for proc in psutil.process_iter(['cmdline', 'name']):
                    if proc.name().startswith("MuMu"):
                        proc.terminate()
                        proc.wait(timeout=5)
                login_verify()
            else:
                fill_login_box()
                login_verify()
        # 不需要登出时的进入游戏
        else:
            self.ocr.text("进入游戏")
            if self.ocr.text("账号密码", blocking=0, region_id=5):
                fill_login_box()
            else:
                self.ocr.click_text("进入游戏")
            login_verify()
