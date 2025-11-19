class Account:
    """the account entity refers to the json files in resources//account"""

    def __init__(self):
        """define the attributes for the class Account, the uid is the primary key"""
        self.uid = ""
        self.channel = ""
        self.account = ""
        self.password = ""
        # among all account objects, there could only one object's login is 1, others should be 0
        self.login = 0

    def __eq__(self, other):
        """define the equation between Account objects, if the uid is same, the objects is same

        Args:
            other (Object): the other object for comparaing

        Returns:
            boolean: whether the other object is the same with the current object
        """
        if isinstance(other, Account):
            return self.uid == other.uid
        return False
