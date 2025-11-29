class Account:
    def __init__(self):
        """记录用户账户信息的类
        """
        self.uid = ""
        self.channel = ""
        self.account = ""
        self.password = ""
        # 所有的account objects中，只有一个的login可为1，其余为0
        self.login = False

    def __eq__(self, other):
        """定义account与其它object之间的比较，uid相同则相同

        Args:
            other (object): 比较的object

        Returns:
            boolean: True为同一个account
        """
        if isinstance(other, Account):
            return self.uid == other.uid
        return False
