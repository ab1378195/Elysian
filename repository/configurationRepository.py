import os
from json import load, dump


class ConfigurationRepository:
    def __init__(self):
        """管理各项配置读写的类"""
        self.resource_path = os.path.join("resources", "configuration")

    def get_configuration(self, configuration_name):
        """获取指定配置的配置信息

        Args:
            configuration_name (String): 配置文件名称(不含.json)

        Returns:
            dict: 配置信息字典，未找到返回{ }
        """
        try:
            with open(
                os.path.join(self.resource_path, configuration_name + ".json"),
                "r",
                encoding="utf-8",
            ) as f:
                configuration = load(f)
            return configuration
        except FileNotFoundError:
            return {}

    def save_configuration(self, configuration, configuration_name):
        """保存指定配置的配置信息

        Args:
            configuration (dict): 配置信息
            configuration_name (String): 配置文件名称(不含.json)
        """
        with open(
            os.path.join(self.resource_path, configuration_name + ".json"),
            "w",
            encoding="utf-8",
        ) as f:
            dump(configuration, f, ensure_ascii=False, indent=4)
