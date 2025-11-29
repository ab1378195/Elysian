from repository.accountRepository import AccountRepository


class AccountService:
    def __init__(self):
        """处理account相关业务逻辑的类
        """
        self.accountRepository = AccountRepository()

    def find_all_account(self):
        """找到所有的account，并作为列表返回

        Returns:
            List<Account>: account列表(未找到返回[ ])
        """
        return self.accountRepository.find_all_account()

    def save(self, account):
        """保存一个account

        Args:
            account (Account): 需要保存的account
        """
        self.accountRepository.save(account)

    def delete(self, uid):
        """根据uid删除指定的account

        Args:
            uid (String): 要删除account的uid
        """
        self.accountRepository.delete(uid)

    def update_login_account(self, uid):
        """更新登录账户

        Args:
            uid (String): 新登录账户的uid
        """
        account_list = self.find_all_account()
        for account in account_list:
            if account.uid == uid:
                account.login = True
                self.save(account)
            elif account.login:
                account.login = False
                self.save(account)

    def get_login_account(self):
        """找到登录账户，未找到返回None

        Returns:
            Optional<Account>: 登录account|None
        """
        account_list = self.find_all_account()
        for account in account_list:
            if account.login:
                return account
        return None
