class Strategy:
    def __init__(self):
        self.name = ""
        self.name_ch = ""
        self.combat_strategy = {}
        self.engraving_strategy = {}

    def __eq__(self, other):
        if isinstance(other, Strategy):
            return self.name == other.name
        return False