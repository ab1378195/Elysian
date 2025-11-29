class Strategy:
    def __init__(self):
        """记录女武神策略信息的类"""
        self.name = ""
        self.name_ch = ""
        self.combat_strategy = {}
        self.engraving_strategy = {}

    def __eq__(self, other):
        """定义strategy其它object之间的比较，name相同则相同

        Args:
            other (object): 比较的object

        Returns:
            boolean: 相同返回True
        """
        if isinstance(other, Strategy):
            return self.name == other.name
        return False
