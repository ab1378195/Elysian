import os
from model.strategy import Strategy
from json import load, dump


class StrategyRepository:
    def __init__(self):
        """管理strategy读写操作的类"""
        self.resource_path = os.path.join(
            os.path.join("resources", "realm"), "strategy"
        )

    def find_all_strategy(self):
        """找到所有的strategy，并返回列表

        Returns:
            List<Strategy>: 包含所有strategy的列表，未找到返回[ ]
        """
        strategy_list = []
        for filename in os.listdir(self.resource_path):
            with open(
                os.path.join(self.resource_path, filename), "r", encoding="utf-8"
            ) as f:
                strategy_info = load(f)
            strategy = Strategy(
                os.path.splitext(filename)[0], list(strategy_info.values())
            )
            strategy_list.append(strategy)
        return strategy_list

    def get_strategy(self, name):
        """根据name获得指定的strategy

        Args:
            name (String): strategy的name(英文文件名)

        Returns:
            Strategy: 对应name的strategy
        """
        with open(
            os.path.join(self.resource_path, name + ".json"), "r", encoding="utf-8"
        ) as f:
            strategy_info = load(f)
        strategy = Strategy(name, list(strategy_info.values()))
        return strategy
