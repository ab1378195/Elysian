from repository.recordRepository import RecordRepository


class RecordService:
    def __init__(self):
        """处理记录相关业务逻辑的类"""
        self.recordRepository = RecordRepository()

    def get_material_record(self):
        """获取材料活动任务的记录

        Returns:
            dict: 材料活动记录的字典，未找到返回{ }
        """
        return self.recordRepository.get_record("material")

    def save_material_record(self, record):
        """保存材料活动任务的新记录

        Args:
            record (dict): 要保存的记录信息
        """
        self.recordRepository.save_record("material", record)

    def get_home_record(self):
        """获取家园日常任务的记录

        Returns:
            dict: 家园日常任务记录的字典，未找到返回{ }
        """
        return self.recordRepository.get_record("home")

    def save_home_record(self, record):
        """保存家园日常任务的新记录

        Args:
            record (dict): 要保存的记录信息
        """
        self.recordRepository.save_record("home", record)
