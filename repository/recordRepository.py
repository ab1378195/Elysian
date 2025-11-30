import os
from json import load, dump


class RecordRepository:
    def __init__(self):
        """用于读写各项任务记录的类"""
        self.resource_path = os.path.join("resources", "record")

    def get_record(self, record_name):
        """查询指定任务的记录

        Args:
            record_name (String): 记录名称(不含后缀.json)

        Returns:
            dict: 记录信息，未查询到返回{ }
        """
        try:
            with open(
                os.path.join(self.resource_path, record_name + ".json"),
                "r",
                encoding="utf-8",
            ) as f:
                record = load(f)
            return record
        except:
            return {}

    def save_record(self, record_name, record):
        """保存指定任务的记录

        Args:
            record_name (String): 记录名称(不含后缀.json)
            record (dict): 要保存的记录信息
        """
        with open(
            os.path.join(self.resource_path, record_name + ".json"),
            "w",
            encoding="utf-8",
        ) as f:
            dump(record, f, ensure_ascii=False, indent=4)
