from repository.configurationRepository import ConfigurationRepository


class ConfigurationService:
    def __init__(self):
        """处理配置相关业务逻辑的类"""
        self.configurationRepository = ConfigurationRepository()

    def get_task_configuration(self):
        """获取上次执行的任务清单配置信息

        Returns:
            dict: 上次执行的任务清单信息字典，未找到返回{ }
        """
        return self.configurationRepository.get_configuration("task")

    def save_task_configuration(self, configuration):
        """保存执行的任务清单

        Args:
            configuration (dict): 任务清单信息字典
        """
        self.configurationRepository.save_configuration(configuration, "task")

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

    def __configuration_validate(self, default_configuration, configuration_name):
        """校验指定配置文件是否存在，如果存在返回已有配置，否则创建配置文件并写入默认配置

        Args:
            default_configuration (dict): 默认配置字典
            configuration_name (String): 配置文件名称

        Returns:
            dict: 配置文件信息
        """
        configuration = self.configurationRepository.get_configuration(
            configuration_name
        )
        if not configuration:
            self.configurationRepository.save_configuration(
                default_configuration, configuration_name
            )
            configuration = self.configurationRepository.get_configuration(
                configuration_name
            )
        return configuration

    def get_material_configuration(self):
        """获取材料活动相关配置信息

        Returns:
            dict: 材料活动配置信息字典，未找到返回默认配置
        """
        return self.__configuration_validate({"frequency": "每日一次"}, "material")

    def save_material_configuration(self, configuration):
        """保存材料活动相关配置信息

        Args:
            configuration (dict): 材料活动配置信息
        """
        self.configurationRepository.save_configuration(configuration, "material")

    def get_home_configuration(self):
        """获取家园日常的配置信息

        Returns:
            dict: 家园日常的配置信息字典，未找到返回默认配置
        """
        return self.__configuration_validate(
            {"reward": "每次启动", "quest": "每日一次", "storysweep": ["每日一次", 3]},
            "home",
        )

    def save_home_configuration(self, configuration):
        """保存家园日常的配置

        Args:
            configuration (dict): 家园日常的配置字典
        """
        self.configurationRepository.save_configuration(configuration, "home")

    def get_commission_configuration(self):
        """获取舰团委托的配置信息

        Returns:
            dict: 舰团委托的配置字典
        """
        return self.__configuration_validate(
            {"frequency": "每日一次", "times": "4"}, "commission"
        )

    def save_commission_configuration(self, configuration):
        """保存舰团委托的配置

        Args:
            configuration (dict): 舰团委托的配置字典
        """
        self.configurationRepository.save_configuration(configuration, "commission")

    def save_realm_configuration(self, configuration):
        """保存往世乐土相关配置信息

        Args:
            configuration (dict): 往世乐土的新配置信息
        """
        self.configurationRepository.save_configuration(configuration, "realm")

    def get_realm_configuration(self):
        """获取往世乐土相关配置信息

        Returns:
            dict: 往世乐土配置信息字典，未找到返回默认配置
        """
        return self.__configuration_validate(
            {
                "name_ch": "真我·人之律者",
                "level": "终尽(2.75)",
                "name": "Herrscher_of_Human",
            },
            "realm",
        )
