from repository.strategyRepository import StrategyRepository


class StrategyService:
    def __init__(self):
        """处理strategy相关业务逻辑的类"""
        self.strategyRepository = StrategyRepository()

    def find_all_strategy(self):
        """找到所有的strategy，并返回列表

        Returns:
            List<Strategy>: 包含所有strategy的列表，未找到返回[ ]
        """
        return self.strategyRepository.find_all_strategy()

    def get_strategy(self, name):
        """根据name获得指定的strategy

        Args:
            name (String): strategy的name(英文文件名)

        Returns:
            Strategy: 对应name的strategy
        """
        return self.strategyRepository.get_strategy(name)
