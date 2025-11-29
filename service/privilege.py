import ctypes, sys


def adminPermissionAcquire():
    """如果没有管理员权限，申请管理员权限"""

    def adminPermissionCheck():
        """检查是否拥有管理员权限

        Returns:
            int: 1代表拥有管理员权限，0代表没有
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return 0

    if not adminPermissionCheck():
        # 通过管理员权限重启程序以获取管理员权限
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
        sys.exit()  # 终止当前程序
