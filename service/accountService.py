from repository.accountRepository import AccountRepository


class AccountService:
    """the service layer for manipulating the account objects"""

    def __init__(self):
        """basic attributes"""
        self.accountRepository = AccountRepository()

    def findAll(self):
        """find all Account objects

        Returns:
            List<Account>: a list of all Account objects
        """
        return self.accountRepository.findAll()

    def save(self, account):
        """save a account object

        Args:
            account (Account): the Account object needs to be saved
        """
        self.accountRepository.save(account)

    def delete(self, uid):
        """delete the Account object by uid

        Args:
            uid (String): the uid of the deleting object
        """
        self.accountRepository.delete(uid)

    def update_login_account(self, uid):
        """update the login attribute of account with specific uid to 1, and make other account objects' login attribute to 0

        Args:
            uid (String): the uid of new login Account object
        """
        account_list = self.findAll()
        for account in account_list:
            if account.uid == uid:
                account.login = 1
                self.save(account)
            elif account.login == 1:
                account.login = 0
                self.save(account)

    def get_login_account(self):
        """find the login account, if no login account, return None

        Returns:
            Optional<Account>: the login account / None
        """
        account_list = self.findAll()
        for account in account_list:
            if account.login == 1:
                return account
        return None
    
    def save_emulator_config(self, config_info):
        self.accountRepository.saveEmulatorConfig(config_info)

    def get_emulator_config(self):
        return self.accountRepository.getEmulatorConfig()
