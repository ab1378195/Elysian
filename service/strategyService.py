from repository.strategyRepository import StrategyRepository

class StrategyService:
    def __init__(self):
        self.strategyRepository = StrategyRepository()

    def findAll(self):
        return self.strategyRepository.findAll()
    
    def getConfig(self):
        return self.strategyRepository.getConfig()
    
    def saveConfig(self, config_info):
        self.strategyRepository.saveConfig(config_info)