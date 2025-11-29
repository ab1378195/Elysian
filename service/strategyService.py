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
