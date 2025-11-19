import os
from model.strategy import Strategy
from json import load, dump


class StrategyRepository:
    def __init__(self):
        self.resource_path = "resources//Elysian"
        self.exclude_list = ["portal.pt", "config.json"]

    def findAll(self):
        strategy_list = []
        for filename in os.listdir(self.resource_path):
            if filename in self.exclude_list:
                continue
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

    def getConfig(self):
        with open(os.path.join(self.resource_path,"config.json"),"r",encoding="utf-8") as f:
            config_info = load(f)
        return config_info
    
    def saveConfig(self, config_info):
        strategy_list = self.findAll()
        for strategy in strategy_list:
            if config_info["name_ch"] == strategy.name_ch:
                config_info["name"] = strategy.name
        with open(os.path.join(self.resource_path,"config.json"),"w",encoding="utf-8") as f:
            dump(config_info, f, ensure_ascii=False, indent=4)