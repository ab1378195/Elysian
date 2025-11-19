from json import load, dump
import os
from model.account import Account


class AccountRepository:
    """the repository for CURD operations for Account objects"""

    def __init__(self):
        """basic attributes"""
        self.resource_path = "resources//account"
        self.exclude_list = ["emulator.json"]

    def save(self, account):
        """save a new account object

        Args:
            account (Account): a new Account object needs to be stored
        """
        account_data = {
            "channel": account.channel,
            "account": account.account,
            "password": account.password,
            "login": account.login,
        }
        with open(
            self.resource_path + "//" + account.uid + ".json", "w", encoding="utf-8"
        ) as f:
            dump(account_data, f, ensure_ascii=False, indent=4)

    def findAll(self):
        """find all Account objects

        Returns:
            List<Account>: a list of all Account objects
        """
        account_list = []
        for filename in os.listdir(self.resource_path):
            if filename in self.exclude_list:
                continue
            account = Account()
            with open(self.resource_path + "//" + filename, "r", encoding="utf-8") as f:
                account_info = load(f)
            account.uid = filename[:-5]
            account.account = account_info["account"]
            account.password = account_info["password"]
            account.channel = account_info["channel"]
            account.login = account_info["login"]
            account_list.append(account)
        return account_list

    def delete(self, uid):
        """delete the account with uid (primary key)

        Args:
            uid (String): uid of the object
        """
        if os.path.exists(self.resource_path + "//" + uid + ".json") and os.path.isfile(
            self.resource_path + "//" + uid + ".json"
        ):
            os.remove(self.resource_path + "//" + uid + ".json")

    def saveEmulatorConfig(self, config_info):
        with open(
            os.path.join(self.resource_path, "emulator.json"), "w", encoding="utf-8"
        ) as f:
            dump(config_info, f, ensure_ascii=False, indent=4)

    def getEmulatorConfig(self):
        try:
            with open(os.path.join(self.resource_path, "emulator.json"),"r", encoding="utf-8") as f:
                config_info = load(f)
            return config_info
        # might not have the file (first run)
        except:
            return {}
