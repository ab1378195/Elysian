from service.strategyService import StrategyService

class Elysian:
    def __init__(self, log_queue):
        strategyService = StrategyService()
        self.config_info = strategyService.getConfig()
        self.log_queue = log_queue

    def run(self):
        self.log_queue.put(["开始执行往世乐土深层序列任务","INF2"])
        