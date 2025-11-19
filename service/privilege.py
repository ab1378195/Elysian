import ctypes, sys


def adminPermissionAcquire():
    """acquire admin permission if not
    """
    def adminPermissionCheck():
        """check admin permission\n
        `Returns`: 1 means have admin permission, 0 means not
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return 0

    if not adminPermissionCheck():
        # restart the program with admin permission
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
        sys.exit()  # terminate current program
