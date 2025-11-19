from plyer import notification


class Notification:
    """the class to show a system notification"""

    def __init__(self):
        """basic attributes"""
        self.icon = "resources\\ui\\logo.ico"

    def info(self, title, message):
        """show a system notification with given title and message

        Args:
            title (String): the title of the notification
            message (String): the message of the notification
        """
        notification.notify(title=title, message=message, app_icon=self.icon, timeout=5)
