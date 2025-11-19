import winreg
from subprocess import Popen
from pyautogui import click, moveTo, hotkey
import pygetwindow as gw
from utils.ocr import OCR
from time import sleep
from service.accountService import AccountService
from utils.imageFinder import ImageFinder
from math import pow
from pyperclip import copy
from api.mumu.mumu import Mumu


class Launch:
    def __init__(self, log_queue):
        accountService = AccountService()
        self.account = accountService.get_login_account()
        if self.account.channel == "渠道服":
            self.emulator_info = accountService.get_emulator_config()
        self.logout = False
        self.log_queue = log_queue
        self.imgF = ImageFinder()

    def launch_game(self):
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
        self.log_queue.put(["启动成功", "INF2"])
        self.log_queue.put(["exit", "INF1"])

    def activate_game(self):
        active_window = gw.getActiveWindow()
        if active_window.title != "崩坏3":
            game_window = gw.getWindowsWithTitle("崩坏3")
            game_window[0].activate()

    def enter_game(self):
        ocr = OCR()
        # wait until the login is already
        while True:
            self.activate_game()
            sleep(1)
            if ocr.text("进入游戏", 0, region_id=7) == 1:
                sleep(4)
                break
        # need to logout (uid is different)
        if self.logout:
            if self.account.channel == "渠道服":
                self.log_queue.put(["检测到为渠道服账号，登出账号", "INF1"])
            else:
                self.log_queue.put(["检测到uid不符，登出账号", "INF1"])
            # check which login page now and jump to login box in both cases
            while True:
                if ocr.click_text("更换账号", 0, region_id=4) == 1:
                    sleep(1)
                    # choose the option "remain login history"
                    ocr.text("保留", region_id=5)
                    base_position = ocr.find("保留", region_id=5)
                    self.imgF.single(
                        "resources//login//selected_radiobutton.png", region_id=5
                    )
                    distance = pow(self.imgF.position[0] - base_position[0], 2) + pow(
                        self.imgF.position[1] - base_position[1], 2
                    )
                    self.imgF.single(
                        "resources//login//unselected_radiobutton.png", region_id=5
                    )
                    # the unselected box is closer, meaning the option should be choosed
                    if (
                        pow(self.imgF.position[0] - base_position[0], 2)
                        + pow(self.imgF.position[1] - base_position[1], 2)
                        < distance
                    ):
                        moveTo(self.imgF.position)
                        click()
                    # logout
                    sleep(1)
                    ocr.click_text("退出", region_id=5, match=1)
                    sleep(1)
                if ocr.click_text("登录其他账号", 0, 5) == 1:
                    sleep(1)
                    break
                if self.imgF.single("resources//login//QRcode.png"):
                    sleep(1)
                    break
            if self.account.channel == "渠道服":
                self.log_queue.put(["检测到为渠道服登录，启动模拟器", "INF1"])
                mumu = Mumu(self.emulator_info["path"]).select(
                    self.emulator_info["index"]
                )
                mumu.power.start()
                sleep(10)
                mumu.window.show()
                mumu.app.launch("com.github.haocen2004.bh3_login_simulation")
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
                ocr.click_text("扫描二维码")
                sleep(1)
                ocr.click_text("实时")
                sleep(0.5)
                game_window = gw.getWindowsWithTitle("崩坏3")
                game_window[0].activate()
                sleep(5)
                ocr.click_text("进入游戏", region_id=7)
                self.log_queue.put(["检测到登录成功，退出模拟器", "INF1"])
                mumu.power.shutdown()
                sleep(10)
            else:
                # enter account information in login box
                ocr.click_text("账号密码", region_id=5)
                sleep(1)
                ocr.click_text("手机号", region_id=5)
                sleep(0.5)
                copy(self.account.account)
                hotkey("ctrl", "v")
                sleep(0.5)
                ocr.click_text("密码", region_id=5)
                sleep(0.5)
                copy(self.account.password)
                hotkey("ctrl", "v")
                sleep(0.5)
                ocr.click_text("进入游戏", region_id=5)
                # accept user agreements
                while True:
                    sleep(1)
                    if ocr.click_text("同意", blocking=0, region_id=5, match=1):
                        sleep(10)
                    if ocr.text("进入游戏", blocking=0, region_id=7):
                        sleep(3)
                        break
                # select channel
                self.imgF.single("resources//login//channel.png", region_id=7)
                moveTo(self.imgF.position)
                sleep(0.2)
                click()
                sleep(1)
                if self.account.channel == "ios":
                    self.imgF.single("resources//login//ios.png")
                    moveTo(self.imgF.position)
                    sleep(0.2)
                    click()
                else:
                    if self.account.channel == "官服":
                        self.account.channel = "全平台"
                    if self.account.channel == "Android":
                        self.account.channel = "安卓"
                    ocr.click_text(self.account.channel)
                sleep(1)
                ocr.click_text("确定")
                sleep(2)
                ocr.click_text("进入游戏", region_id=7)
                sleep(10)
        # not need to logout (uid is same)
        else:
            ocr.click_text("进入游戏", 0, region_id=7)
            sleep(5)
