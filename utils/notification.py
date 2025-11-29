from plyer import notification


class Notification:
    def __init__(self):
        """显示系统消息的类"""
        self.icon = "resources\\ui\\logo.ico"

    def info(self, title, message):
        """显示一个系统的消息提示

        Args:
            title (String): 消息的标题
            message (String): 消息的内容
        """
        notification.notify(title=title, message=message, app_icon=self.icon, timeout=5)
