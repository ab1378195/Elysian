from repository.configurationRepository import ConfigurationRepository


class ConfigurationService:
    def __init__(self):
        """处理配置相关业务逻辑的类"""
        self.configurationRepository = ConfigurationRepository()

    def save_emulator_configuration(self, configuration):
        """保存模拟器相关配置

        Args:
            configuration (dict): 模拟器的新配置信息
        """
        self.configurationRepository.save_configuration(configuration, "emulator")

    def get_emulator_configuration(self):
        """获取模拟器相关配置信息

        Returns:
            dict: 模拟器配置信息字典，未找到返回{ }
        """
        return self.configurationRepository.get_configuration("emulator")

    def save_Elysian_configuration(self, configuration):
        """保存往世乐土相关配置信息

        Args:
            configuration (dict): 往世乐土的新配置信息
        """
        self.configurationRepository.save_configuration(configuration, "Elysian")

    def get_Elysian_configuration(self):
        """获取往世乐土相关配置信息

        Returns:
            dict: 往世乐土配置信息字典，未找到返回{ }
        """
        return self.configurationRepository.get_configuration("Elysian")
