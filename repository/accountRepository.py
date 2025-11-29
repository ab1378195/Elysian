from json import load, dump
import os
from model.account import Account


class AccountRepository:
    def __init__(self):
        """用于管理account数据读写的类"""
        self.resource_path = os.path.join("resources", "account")

    def save(self, account):
        """保存新的account

        Args:
            account (Account): 需要保存的新account
        """
        account_data = {
            "channel": account.channel,
            "account": account.account,
            "password": account.password,
            "login": account.login,
        }
        with open(
            os.path.join(self.resource_path, account.uid + ".json"),
            "w",
            encoding="utf-8",
        ) as f:
            dump(account_data, f, ensure_ascii=False, indent=4)

    def find_all_account(self):
        """找到所有的account，并作为列表返回

        Returns:
            List<Account>: account列表(未找到返回[ ])
        """
        account_list = []
        for filename in os.listdir(self.resource_path):
            account = Account()
            with open(
                os.path.join(self.resource_path, filename), "r", encoding="utf-8"
            ) as f:
                account_info = load(f)
            account.uid = os.path.splitext(filename)[0]
            account.account = account_info["account"]
            account.password = account_info["password"]
            account.channel = account_info["channel"]
            account.login = account_info["login"]
            account_list.append(account)
        return account_list

    def delete(self, uid):
        """根据uid删除对应的account

        Args:
            uid (String): account的uid属性
        """
        os.remove(os.path.join(self.resource_path, uid + ".json"))
