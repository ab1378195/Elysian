import win32gui, win32ui
from ctypes import windll
from PIL import Image


class Screenshot:
    def __init__(self):
        """获取崩坏3截图的类，必须要存在崩坏3窗口"""
        windll.shcore.SetProcessDpiAwareness(1)
        self.hwnd = win32gui.FindWindow(None, "崩坏3")
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.width = right - left
        self.height = bottom - top

    def screenshot(self):
        """获得崩坏3窗口的截图，并返回PIL的Image

        Returns:
            Image: 截图
        """
        hwndDC = win32gui.GetWindowDC(self.hwnd)  # 窗口的DC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)  # 创建兼容DC
        saveDC = mfcDC.CreateCompatibleDC()  # 创建内存DC用于保存图像
        # 创建位图对象
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, self.width, self.height)
        # 将位图选入内存DC
        saveDC.SelectObject(saveBitMap)
        # 将窗口内容拷贝到内存DC
        result = windll.user32.PrintWindow(self.hwnd, saveDC.GetSafeHdc(), 1)
        # 将位图转换为PIL图像
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        img = Image.frombuffer(
            "RGB",
            (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
            bmpstr,
            "raw",
            "BGRX",
            0,
            1,
        )
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        return img
