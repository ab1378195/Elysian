class Strategy:
    def __init__(self, name, args_list):
        """记录女武神策略信息的类"""
        self.name = name
        self.name_ch = args_list[0]
        self.name_match = args_list[1]
        self.assistance = args_list[2]
        self.double = args_list[3]
        # json只支持tuple,需手动转回python的list
        self.combat_strategy = list(args_list[4])
        self.engraving_strategy = list(args_list[5])
        self.engraving = {
            "Elysia": args_list[6]["Elysia"],
            "Mobius": args_list[6]["Mobius"],
            "Pardofelis": args_list[6]["Pardofelis"],
            "Aponia": args_list[6]["Aponia"],
            "Vill_V": args_list[6]["Vill_V"],
            "Kosma": args_list[6]["Kosma"],
            "Kevin": args_list[6]["Kevin"],
            "Kalpas": args_list[6]["Kalpas"],
            "Eden": args_list[6]["Eden"],
            "Su": args_list[6]["Su"],
            "Hua": args_list[6]["Hua"],
            "Griseo": args_list[6]["Griseo"],
            "Sakura": args_list[6]["Sakura"],
        }
        self.prior = args_list[7]
        self.storybook = args_list[8]

    def __eq__(self, other):
        """定义strategy其它object之间的比较，name相同则相同

        Args:
            other (object): 比较的object

        Returns:
            boolean: 相同返回True
        """
        if isinstance(other, Strategy):
            return self.name == other.name
        return False

    def select_personalized(self, index):
        # 专属刻印在选择后直接从strategy中删除
        engraving = self.engraving["Elysia"].pop(index)
        # 若所有专属刻印已选择，删除Elysia相关的信息
        if not self.engraving["Elysia"]:
            del self.engraving["Elysia"]
            self.engraving_strategy.remove("Elysia")
        return engraving

    def select_core(self, name):
        # 其他英桀的刻印在选择了核心刻印后优先级调至指定位置
        self.engraving_strategy.remove(name)
        self.engraving_strategy.insert(self.prior, name)
