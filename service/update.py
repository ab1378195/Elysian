import requests
from json import load
from tkinter import messagebox
from utils.notification import Notification
from zipfile import ZipFile
import os
import shutil
import sys
from subprocess import Popen, CREATE_NO_WINDOW


class Update:
    def __init__(self):
        self.api_url = "https://api.github.com/repos/ab1378195/Elysian/releases/latest"
        with open("resources//version//version.json", "r", encoding="utf-8") as f:
            version_information = load(f)
        self.current_version = version_information["version"]
        self.environment = version_information["environment"]
        self.new_version = ""
        self.notification = Notification()
        self.download_path = "update.zip"
        self.exclude_list = ["account"]

    def check_update(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            data = response.json()
            self.new_version = data["tag_name"]
            if self.new_version != self.current_version:
                decision = messagebox.askquestion(
                    title="更新提示",
                    message=f"检测到新版本{self.new_version}，是否更新？",
                )
                if decision == "yes":
                    self.download()
        except:
            self.notification.info(title="检查更新失败", message=f"获取远程版本失败")

    def download(self):
        download_url = f"https://github.com/ab1378195/Elysian/releases/download/{self.new_version}/Elysian-{self.environment}-{self.new_version}.zip"
        try:
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            with open(self.download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            self.notification.info(
                title="下载完成", message="下载新版本成功，开始合并文件。"
            )
            self.merge()
        except:
            self.notification.info(title="下载失败", message=f"下载新版本失败")

    def merge(self):
        try:
            extract_path = "temp"
            with ZipFile(self.download_path, "r") as zip:
                zip.extractall(extract_path)
            # deal with the resources first (have excluded files)
            for file in os.listdir(extract_path + "//resources"):
                if file in self.exclude_list:
                    continue
                src = os.path.join(extract_path + "//resources", file)
                dst = os.path.join("resources", file)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                else:
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
            shutil.rmtree(extract_path + "//resources")
            # python can delete itself
            if self.environment == "Python":
                # deal with normal files
                for file in os.listdir(extract_path):
                    src = os.path.join(extract_path, file)
                    dst = os.path.join(".", file)
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
                    else:
                        if os.path.exists(dst):
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst)
                os.remove(self.download_path)
                shutil.rmtree(extract_path)
                self.notification.info(title="更新完成", message="新版本合并完成。")
                # restart the program
                os.execv(sys.executable, ["python"] + sys.argv)
            # exe needs to have a bat for help
            elif self.environment == "EXE":
                bat_content = f"""
@echo off
chcp 65001 > nul
set "OLD_PATH=%~dp0"
set "TEMP_PATH=%OLD_PATH%temp"
timeout /t 3 /nobreak >nul
if exist "%OLD_PATH%Elysian.exe" (
    del /f /q "%OLD_PATH%Elysian.exe"
)
if exist "%TEMP_PATH%\\Elysian.exe" (
    move /y "%TEMP_PATH%\\Elysian.exe" "%OLD_PATH%" > nul
)
rd /s /q "%TEMP_PATH%" 2>nul
start "" "%OLD_PATH%Elysian.exe"
del "%~f0" 
"""
                with open("update.bat", "w", encoding="utf-8") as f:
                    f.write(bat_content)
                os.remove(self.download_path)
                Popen("update.bat", shell=True, creationflags=CREATE_NO_WINDOW)
                os._exit(0)
        except:
            self.notification.info(title="合并失败", message="合并新版本文件失败")
