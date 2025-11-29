import os
from model.strategy import Strategy
from json import load, dump


class StrategyRepository:
    def __init__(self):
        """管理strategy读写操作的类"""
        self.resource_path = os.path.join("resources", "strategy")

    def find_all_strategy(self):
        """找到所有的strategy，并返回列表

        Returns:
            List<Strategy>: 包含所有strategy的列表，未找到返回[ ]
        """
        strategy_list = []
        for filename in os.listdir(self.resource_path):
            strategy = Strategy()
            with open(
                os.path.join(self.resource_path, filename), "r", encoding="utf-8"
            ) as f:
                strategy_info = load(f)
            strategy.name = os.path.splitext(filename)[0]
            strategy.name_ch = strategy_info["name_ch"]
            strategy.combat_strategy = strategy_info["combat_strategy"]
            strategy.engraving_strategy = strategy_info["engraving_strategy"]
            strategy_list.append(strategy)
        return strategy_list
