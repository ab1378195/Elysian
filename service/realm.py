from service.strategyService import StrategyService
from utils.ocr import OCR
from utils.imageFinder import ImageFinder
from utils.screenshot import Screenshot
from service.configurationService import ConfigurationService
from time import sleep
from pyautogui import size, dragRel, moveTo, click, moveRel, press, keyDown, keyUp
import os
from threading import Event, Thread
from api.portal import portal

NAME_DICTIONARY = {
    "Elysia": ["真我", "爱莉希雅"],
    "Mobius": ["无限", "梅比乌斯"],
    "Pardofelis": ["空梦", "帕朵菲利斯"],
    "Aponia": ["戒约", "阿波尼亚"],
    "Vill_V": ["螺旋", "维尔薇"],
    "Kosma": ["旭光", "科斯魔"],
    "Kevin": ["救世", "凯文"],
    "Kalpas": ["灭", "千劫"],
    "Eden": ["黄金", "伊甸"],
    "Su": ["天慧", "苏"],
    "Hua": ["浮生", "华"],
    "Griseo": ["繁星", "格蕾修"],
    "Sakura": ["刹那", "樱"],
    "Store": ["商店", "商店"],
    "Lock": ["Lock", "Lock"],
    "Boss": ["Boss", "Boss"],
}
NAME_DICTIONARY_CH = {
    "真我": "Elysia",
    "无限": "Mobius",
    "空梦": "Pardofelis",
    "戒约": "Aponia",
    "螺旋": "Vill_V",
    "旭光": "Kosma",
    "救世": "Kevin",
    "灭": "Kalpas",
    "黄金": "Eden",
    "天慧": "Su",
    "浮生": "Hua",
    "繁星": "Griseo",
    "刹那": "Sakura",
}
ENGRAVING_DICTIONATY = {
    "Kevin": {
        "金杯": "施予者的金杯",
        "坠饰": "守望者的坠饰",
        "烙印": "不死者的烙印",
        "假面": "猎杀者的假面",
        "圣器": "制约者的圣器",
        "法衣": "求道者的法衣",
        "1": "救世者的王剑",
        "集": "救世者的麝集",
        "远征": "救世者的远征",
        "余响": "救世者的余响",
        "2": "救世者的孤影",
        "残梦": "救世者的残梦",
        "决断": "救世者的决断",
        "凯旋": "救世者的凯旋",
    },
    "Aponia": {
        "背叛": "其一不可背叛",
        "欺瞒": "其二不可欺瞒",
        "暴": "其三不可暴戾",
        "妄行": "其四不可妄行",
        "伪言": "其五不可伪言",
        "沉沦": "其六不可沉沦",
        "1": "汝当受万般戒律",
        "束": "汝当以此身为束",
        "契": "汝当以此身为契",
        "证": "汝当以此命为证",
        "2": "汝当为戒律所佑",
        "恶": "汝当见诸恶得惩",
        "善": "汝当见诸善得行",
        "愿": "汝当见诸愿得归",
    },
    "Eden": {
        "乐园": "乐园的宣叙",
        "溪流": "溪流的宣叙",
        "飞鸟": "飞鸟的宣叙",
        "果林": "果林的宣叙",
        "美酒": "美酒的宣叙",
        "宝玉": "宝玉的宣叙",
        "1": "黄金的咏叹",
        "丰": "丰壤的咏叹",
        "生命": "生命的咏叹",
        "黎明": "黎明的咏叹",
        "2": "黄金的余音",
        "枯": "枯壤的余音",
        "风": "凄风的余音",
        "夜": "寂夜的余音",
    },
    "Vill_V": {
        "魔术": "第一幕魔术",
        "钟摆": "第二幕钟摆",
        "矛盾": "第三幕矛盾",
        "汤匙": "第四幕汤匙",
        "蛛丝": "第五幕蛛丝",
        "笑": "第六幕嗤笑",
        "1": "幕间剧逆转的螺旋",
        "门": "第七幕虚掩的门扉",
        "厅堂": "第八幕伪饰的厅堂",
        "真相": "最终幕破碎的真相",
        "2": "幕间剧颠末的螺旋",
        "监牢": "木偶剧爻错的监牢",
        "始源": "严肃剧沉眠的始源",
        "指针": "传奇剧交叠的指针",
    },
    "Kalpas": {
        "剑": "剑锋剑冢剑痕",
        "赤": "赤骨赤血赤练",
        "狂信": "狂信狂人狂言",
        "路": "命路命舛命刻",
        "无心": "无妄无心无归",
        "唯神": "唯神唯我唯一",
        "1": "鏖斗鏖战鏖杀鏖灭",
        "鬼": "非人非鬼非神非天",
        "面": "一人一面一契一途",
        "难": "千钧千转千难千劫",
        "2": "鏖兵鏖剪鏖馘鏖灭",
        "死": "无死无生无灭无存",
        "故": "故土故国故友故人",
        "焚": "焚身焚骨焚心焚魂",
    },
    "Su": {
        "宿命": "宿命之箴言",
        "天眼": "天眼之箴言",
        "天耳": "天耳之箴言",
        "他心": "他心之箴言",
        "神足": "神足之箴言",
        "漏足": "漏足之箴言",
        "1": "天慧之真言",
        "无常": "无常之真言",
        "无我": "无我之真言",
        "寂静": "寂静之真言",
        "2": "天慧之秘言",
        "无常之秘言": "无常之秘言",
        "无我之秘言": "无我之秘言",
        "寂静之秘言": "寂静之秘言",
    },
    "Sakura": {
        "梅": "缭乱百花之梅",
        "红叶": "缭乱百花红叶",
        "牡丹": "缭乱百花牡丹",
        "菊": "缭乱百花菊",
        "藤": "缭乱百花藤",
        "菖蒲": "缭乱百花菖蒲",
        "1": "刹那一刀樱上幕",
        "雨": "刹那一刀雨四光",
        "月见酒": "刹那一刀月见酒",
        "猪": "刹那一刀猪鹿蝶",
        "2": "刹那一刀苦夜叉",
        "森罗": "刹那一刀一瞬森罗",
        "无间": "刹那一刀无间恶刹",
        "万象": "刹那一刀万象无明",
    },
    "Kosma": {
        "爪": "亵渎不归之爪",
        "翼": "掩蔽血月之翼",
        "角": "撕裂暗空之角",
        "眼": "俯视邪渊之眼",
        "息": "毁谤硫磺之息",
        "心": "逆结七罪之心",
        "1": "旭光长明不落",
        "英雄": "英雄独担兴衰",
        "难渡": "善恶两分难渡",
        "未易": "宿诺百折未易",
        "2": "旭光长夜孤悬",
        "黎明": "黎明独待皆尽",
        "抉择": "抉择两全追憾",
        "本念": "本念千摧难改",
    },
    "Mobius": {
        "利齿": "利齿的V",
        "缠环": "缠环的P",
        "静默": "静默的B",
        "吻毒": "吻毒的E",
        "栖影": "栖影的C",
        "暗瞳": "暗瞳的T",
        "1": "无限的X",
        "死亡": "死亡的X",
        "未知": "未知的X",
        "新生": "新生的X",
        "2": "无限的M",
        "代祭": "代祭的M",
        "不灭": "不灭的M",
        "崩落": "崩落的M",
    },
    "Griseo": {
        "红色": "红色的热热的",
        "蓝色": "蓝色的冷冷的",
        "黄色": "黄色的暖暖的",
        "黑色": "黑色的暗暗的",
        "白色": "白色的亮亮的",
        "灰色": "灰色的空空的",
        "1": "像是繁星闪耀着的",
        "野花": "像是野花绽放着的",
        "火焰": "像是火焰燃烧着的",
        "叶子": "像是叶子舒展着的",
        "2": "像是繁星黯淡了的",
        "飞散": "像是野花飞散了的",
        "飘落": "像是叶子飘落了的",
        "熄灭": "像是火焰熄灭了的",
    },
    "Hua": {
        "行路": "行路漫漫",
        "日月": "日月蹉跎",
        "玄衣": "玄衣不再",
        "旧梦": "旧梦如昨",
        "纵使": "纵使寻得",
        "言说": "与谁言说",
        "1": "浮生历历百态无常",
        "红尘": "红尘碌碌一梦黄粱",
        "奈何": "无可奈何繁华落尽",
        "相识": "似曾相识却又相忘",
        "2": "浮生茫茫百态皆苦",
        "凡尘": "凡尘总总一苇难渡",
        "如羽": "如羽随风似浪逐流",
        "梦醒": "怎堪梦醒难觅归途",
    },
    "Pardofelis": {
        "猫猫": "猫猫之箴言",
        "刚刃": "刚刃逆卷之尾",
        "宣叙": "街巷的宣叙",
        "灵动": "灵动的P&C",
        "哲学": "行商者的哲学",
        "值钱": "值钱的闪闪的",
        "1": "空梦空集空我空欢",
        "老板": "即兴短剧老板",
        "拳": "刹那一爪猫猫拳",
        "绝": "咱此地命不该绝",
        "2": "空幻空灵空想空梦",
        "即兴": "即兴魔术归零",
        "雪": "刹那一爪雪里藏",
        "早晚": "咱早晚美梦成真",
    },
}
CLS_LIST = [
    "Elysia",
    "Mobius",
    "Pardofelis",
    "Boss",
    "Lock",
    "Aponia",
    "Vill_V",
    "Kosma",
    "Kevin",
    "Kalpas",
    "Store",
    "Eden",
    "Su",
    "Hua",
    "Griseo",
    "Sakura",
]


class Realm:
    def __init__(self, log_queue):
        """执行往世乐土任务的类

        Args:
            log_queue (Queue): 与procedure通信的队列
        """
        self.log_queue = log_queue
        self.ocr = OCR()
        self.imgF = ImageFinder()
        self.img_path = os.path.join(os.path.join("resources", "realm"), "image")
        configurationService = ConfigurationService()
        configuration = configurationService.get_realm_configuration()
        self.level = configuration["level"][:2]  # 只取前两个字，数字和括号不取
        strategyService = StrategyService()
        self.strategy = strategyService.get_strategy(configuration["name"])
        width, height = size()
        self.CENTER_X = width >> 1
        self.CENTER_Y = height >> 1
        self.screenshot = Screenshot()
        self.detector = portal.YoloDetector(
            os.path.join(
                os.path.join(os.path.join("resources", "realm"), "model"), "portal.onnx"
            ),
            "崩坏3",
        )
        self.TARGET_Y = (
            self.CENTER_Y >> 1
        )  # 目标调整的视角Y值(识别到的传送门Y值需小于该值)
        # 目标传送门的X范围限制
        self.TARGET_X_LEFT = self.CENTER_X - 100
        self.TARGET_X_RIGHT = self.CENTER_X + 100

    def run(self):
        """执行往世乐土任务"""
        self.log_queue.put(["开始执行往世乐土深层序列任务", "INF2"])
        self.enter_realm()
        self.log_queue.put(["已进入乐土界面", "INF1"])
        self.ocr.click_text("深层序列", region_id=2)
        sleep(2)
        self.configure_realm()
        sleep(10)
        self.ocr.text("真我", region_id=6)  # 等待专属刻印选择页面出现
        self.__burden_reduction_layer()
        # 后续层数
        # 祸斗层
        self.__normal_layer()
        self.log_queue.put(["第8层已完成", "INF2"])
        # 如果携带故事书,该层去商店替换故事书
        if self.strategy.storybook:
            self.__store_layer()
        else:
            self.__normal_layer()
        self.log_queue.put(["第9层已完成", "INF2"])
        for i in range(10, 16):
            self.__normal_layer()
            self.log_queue.put(["第{}层已完成".format(i), "INF2"])
        self.log_queue.put(["往世乐土深层序列任务执行完成", "INF2"])
        self.__exit_thread()

    def __exit_thread(self):
        """安全退出该线程，确保ocr进程关闭"""
        self.ocr.terminate()
        self.log_queue.put(["exit", "INF1"])

    def __scroll_down(self, times):
        """向下翻动指定次数

        Args:
            times (int): 翻动次数
        """
        for _ in range(times):
            moveTo(self.CENTER_X, self.CENTER_Y)
            sleep(0.2)
            dragRel(0, -300, duration=1)
            sleep(0.5)
        sleep(1)

    def __scroll_up(self, times):
        """向上翻动指定次数

        Args:
            times (int): 翻动次数
        """
        for _ in range(times):
            moveTo(self.CENTER_X, self.CENTER_Y)
            sleep(0.2)
            dragRel(0, 300, duration=1)
            sleep(0.5)
        sleep(1)

    def enter_realm(self):
        """进入乐土的序列选择界面"""
        self.ocr.click_text("出击", region_id=9)
        sleep(1)
        self.ocr.click_text("挑战", region_id=2)
        sleep(1.5)
        self.ocr.click_text("往世", region_id=4)
        sleep(2)
        self.ocr.click_text("出击", region_id=4)

    def configure_realm(self):
        """配置深层序列的战斗配置，包括增益，女武神，助战选择"""

        def configure_role():
            """配置出战女武神

            Returns:
                boolean: True代表找到并配置了出战女武神
            """
            self.ocr.text("出战位", region_id=1)
            sleep(0.2)
            moveRel(0, 200)
            sleep(0.2)
            click()
            sleep(1)
            while True:
                if self.imgF.single(
                    os.path.join(self.img_path, "filter.png"), region_id=3
                ):
                    break
                sleep(0.5)
            moveTo(self.imgF.position)
            sleep(0.2)
            click()
            sleep(0.5)
            # 先拉到最上面
            for _ in range(4):
                moveTo(self.CENTER_X, self.CENTER_Y)
                sleep(0.2)
                dragRel(0, 300, duration=1)
                sleep(0.5)
            # 向下拉到显示角色名字
            for _ in range(2):
                moveTo(self.CENTER_X, self.CENTER_Y)
                sleep(0.2)
                dragRel(0, -200, duration=1)
                sleep(0.5)
            sleep(1)
            self.ocr.click_text(self.strategy.name_match[0])
            sleep(0.5)
            self.ocr.click_text("确认", region_id=4)
            sleep(0.5)
            while True:
                position_list = self.ocr.find_all("级")
                if position_list:
                    break
                sleep(0.5)
            sleep(1)
            # 如果一开始不显示队长而是女武神名字，说明已默认选择了一个，删除列表中第一个位置并直接执行一次名字判断
            if self.ocr.find("队长", region_id=4) is None:
                position_list.pop(0)
                if self.ocr.find(self.strategy.name_match[1], region_id=4) is not None:
                    self.ocr.click_text("确定", region_id=4)
                    sleep(2)
                    return True
            for position in position_list:
                moveTo(position)
                sleep(0.2)
                click()
                sleep(1)
                if self.ocr.find(self.strategy.name_match[1], region_id=4) is not None:
                    self.ocr.click_text("确定", region_id=4)
                    sleep(2)
                    return True
            return False

        def configure_assistance():
            """配置支援女武神"""

            def validate_selection():
                """检测选中的目标女武神的状态

                Returns:
                    boolean: True代表正常选中,False代表位置错误(目标女武神在另外一个槽位已被选中)
                """
                while True:
                    if self.ocr.find("移除", region_id=4) is not None:
                        self.ocr.click_text("返回", region_id=1)
                        sleep(1)
                        self.log_queue.put(["目标支援女武神已选中", "INF1"])
                        return True
                    if self.ocr.find("队伍", region_id=4) is not None:
                        self.ocr.click_text("返回", region_id=1)
                        sleep(1)
                        self.log_queue.put(["目标支援女武神已在队中", "INF1"])
                        return False
                    if self.ocr.click_text("选择", region_id=4):
                        sleep(1)
                        self.log_queue.put(["目标支援女武神已成功选择", "INF1"])
                        return True
                    sleep(0.5)

            while True:
                position_list = self.ocr.find_all("支援位")
                if len(position_list) == 2:
                    break
                sleep(0.5)
            # 排序列表，确保顺序为从左往右
            position_list.sort(key=lambda x: x[0])
            i = 0  # i代表匹配第几个支援女武神
            j = 0  # j代表使用第几个支援位
            while i < 2:
                # 点进支援女武神选择界面
                moveTo(position_list[j][0], position_list[j][1] + 200)
                sleep(0.2)
                click()
                sleep(0.5)
                # 翻页到最上面
                moveTo(self.CENTER_X, self.CENTER_Y)
                sleep(0.2)
                dragRel(0, 300, duration=1)
                sleep(0.5)
                # 进行一次匹配
                if self.imgF.single(
                    os.path.join(self.img_path, self.strategy.assistance[i] + ".png")
                ):
                    moveTo(self.imgF.position)
                    sleep(0.2)
                    click()
                    sleep(1)
                    flag = validate_selection()
                # 翻页进行第二次匹配
                else:
                    sleep(0.2)
                    dragRel(0, -300, duration=1)
                    sleep(0.5)
                    if self.imgF.single(
                        os.path.join(
                            self.img_path, self.strategy.assistance[i] + ".png"
                        )
                    ):
                        moveTo(self.imgF.position)
                        sleep(0.2)
                        click()
                        sleep(1)
                        flag = validate_selection()
                    # 第二次匹配也未匹配到
                    else:
                        self.log_queue.put(["支援女武神选择失败，中止任务", "ERR"])
                        self.__exit_thread()
                if flag:
                    i += 1
                    j += 1
                # 如果当前支援女武神已在队中，说明应该在第一个槽位选择第二个助战女武神(此时第一个助战女武神已在第二个槽位)
                else:
                    i += 1

        # 拖拽到最下方
        for _ in range(3):
            moveTo(self.CENTER_X, self.CENTER_Y)
            sleep(0.2)
            dragRel(0, -300, duration=1)
            sleep(0.5)
        sleep(1)
        while True:
            self.imgF.all(os.path.join(self.img_path, "checkbox.png"))
            # 确保至少有两个框
            if len(self.imgF.position) >= 2:
                break
            else:
                sleep(0.5)
        # 只选择最下面两个增益
        moveTo(self.imgF.position[-1])
        sleep(0.2)
        click()
        sleep(0.5)
        # 同一个框会被多次匹配到，因此选择纵坐标差距在50以上的视为第二个框
        base_y = self.imgF.position[-1][1]
        for position in self.imgF.position[::-1]:
            if base_y - position[1] > 50:
                break
        moveTo(position)
        sleep(0.2)
        click()
        sleep(0.5)
        self.log_queue.put(["增益选择完成", "INF1"])
        # 选择关卡难度
        while True:
            if self.imgF.single(
                os.path.join(self.img_path, "combobox.png"), region_id=7
            ):
                break
            sleep(0.5)
        moveTo(self.imgF.position)
        sleep(0.2)
        click()
        sleep(0.5)
        # 这一难度必定出现在滑动框中,作为定位的位置
        while True:
            position = self.ocr.find("沦没", region_id=5)
            if position is not None:
                break
            sleep(0.5)
        sleep(0.5)
        # 拉到最下
        for _ in range(2):
            moveTo(position)
            sleep(0.2)
            dragRel(0, -300, duration=1)
            sleep(0.5)
        sleep(0.5)
        self.ocr.click_text(self.level, region_id=7)
        self.log_queue.put(["关卡难度选择完成", "INF1"])
        sleep(0.5)
        self.ocr.click_text("减负战斗", region_id=4)
        # 选择出战角色
        sleep(2)  # 等待星之环系统激活的提示关闭
        if configure_role():
            self.log_queue.put(["出战女武神已选择", "INF1"])
        else:
            self.log_queue.put(["出战女武神选择失败,中止任务", "ERR"])
            self.__exit_thread()
        # 选择支援角色
        configure_assistance()
        sleep(1)
        self.ocr.click_text("开始战斗", region_id=4)

    def __find_engraving(self, engraving, name):
        if self.ocr.click_text(engraving, blocking=0):
            sleep(0.5)
            press("i")
            sleep(1)
            if name == "Elysia":
                self.log_queue.put(["[{}]已选择".format(engraving), "INF1"])
            else:
                self.log_queue.put(
                    ["[{}]已选择".format(ENGRAVING_DICTIONATY[name][engraving]), "INF1"]
                )
            return True
        return False

    def __select_personalized_engraving(self, reset=False):
        # 判断刻印文本是否过长，如果过长需要翻页才能看到第三个刻印
        scroll_flag = False
        while True:
            position_list = self.ocr.find_all("祝福")
            if position_list:
                break
            sleep(0.5)
        if len(position_list) < 3:
            scroll_flag = True
        # 如果能够刷新刻印(第一层)
        if reset:
            engraving = self.strategy.select_personalized(0)
            while True:
                if scroll_flag:
                    self.__scroll_up(1)
                if self.__find_engraving(engraving, "Elysia"):
                    return
                if scroll_flag:
                    self.__scroll_down(1)
                    if self.__find_engraving(engraving, "Elysia"):
                        return
                press("u")
                sleep(2)
        # 如果不能刷新刻印
        else:
            for i, engraving in enumerate(self.strategy.engraving["Elysia"]):
                if scroll_flag:
                    self.__scroll_up(1)
                if self.__find_engraving(engraving, "Elysia"):
                    self.strategy.select_personalized(i)
                    return
                if scroll_flag:
                    self.__scroll_down(1)
                    if self.__find_engraving(engraving, "Elysia"):
                        self.strategy.select_personalized(i)
                        return
            self.log_queue.put(["未找到目标刻印，中止任务", "ERR"])
            self.__exit_thread()

    def get_current_name(self):
        """获得当前刻印选择页面的英桀英文名

        Returns:
            String: 英桀的英文名
        """
        for name in NAME_DICTIONARY_CH.keys():
            if self.ocr.find(name, region_id=6):
                name_en = NAME_DICTIONARY_CH[name]
                self.log_queue.put(
                    [
                        "检测到当前为[{}]刻印选择".format(NAME_DICTIONARY[name_en][1]),
                        "INF1",
                    ]
                )
                return name_en
        self.log_queue.put(["未检测到英桀名称，中止任务", "ERR"])
        self.__exit_thread()

    def __select_normal_engraving(self):
        name = self.get_current_name()
        for engraving in self.strategy.engraving[name][0]:
            if self.__find_engraving(engraving, name):
                return
        self.log_queue.put(["未找到目标刻印，中止任务", "ERR"])
        self.__exit_thread()

    def __select_core_engraving(self):
        name = self.get_current_name()
        keyDown("shiftleft")
        sleep(0.2)
        press(self.strategy.engraving[name][1])
        sleep(0.2)
        keyUp("shiftleft")
        sleep(1)
        press("i")
        self.strategy.select_core(name)
        self.log_queue.put(
            [
                "核心刻印[{}]选择".format(
                    ENGRAVING_DICTIONATY[name][self.strategy.engraving[name][1]]
                ),
                "INF1",
            ]
        )

    def __burden_reduction_layer(self):
        def select_portal():
            for name in self.strategy.engraving_strategy:
                if self.ocr.click_text(
                    NAME_DICTIONARY[name][0], blocking=0, region_id=6
                ):
                    self.log_queue.put(
                        ["选择了[{}]".format(NAME_DICTIONARY[name][1]), "INF1"]
                    )
                    return
            self.log_queue.put(["未识别到任何英桀的门，中止任务", "ERR"])
            self.__exit_thread()

        self.log_queue.put(["开始减负层部分", "INF1"])
        self.log_queue.put(["第1层开始", "INF1"])
        # 开启简略描述，减少文字匹配难度
        if self.imgF.single(os.path.join(self.img_path, "simple.png"), region_id=2):
            moveTo(self.imgF.position)
            sleep(0.2)
            click()
            sleep(0.5)
        # 先选择专属刻印
        self.__select_personalized_engraving(reset=True)
        # 如果为英桀，首层可选择第二个专属刻印
        if self.strategy.double:
            self.__select_personalized_engraving(reset=True)
        i = 2  # 当前层数
        while True:
            while True:
                # 传送门选择的处理
                if self.ocr.find("传送", region_id=6) is not None:
                    sleep(0.5)
                    self.log_queue.put(["选择第{}层的传送门".format(i), "INF1"])
                    select_portal()
                    i += 1
                    sleep(2)
                    continue
                # 刻印选择的处理
                if self.ocr.find("刻印", region_id=6) is not None:
                    sleep(1)
                    break
                # 减负层已完成
                if self.ocr.find("得分", region_id=1) is not None:
                    self.log_queue.put(["减负层已完成", "INF2"])
                    return
                sleep(0.5)
            self.ocr.text("简略", region_id=2)  # 等待选择刻印页面出现
            # 选择核心刻印
            if self.ocr.find("核心", region_id=2) is not None:
                self.__select_core_engraving()
            # 选择一般刻印
            else:
                self.__select_normal_engraving()
            sleep(2)

    def __portal(self):
        def log_detection(portals):
            log = "识别到了"
            for name in portals.keys():
                log += NAME_DICTIONARY[name][1] + ","
            self.log_queue.put([log[:-1], "INF1"])

        def justify_perspective(portals):
            # 取第一个门的y值判别即可
            position = list(portals.values())[0][0]
            if position[1] > self.TARGET_Y:
                self.log_queue.put(["正在调整视角", "INF1"])
                moveTo(self.CENTER_X, self.CENTER_Y)
                sleep(0.2)
                dragRel(0, 50, duration=1)
                sleep(0.5)
                return False
            self.log_queue.put(["视角调整完毕", "INF2"])
            return True

        def find_all_portal(portals):
            count_left = 0
            count_right = 0
            count_portal = 0
            for name, position in zip(portals.keys(), portals.values()):
                # Boss层仅一个传送门
                if name == "Boss":
                    return 0
                # 其余层除store外应有三个门
                if position[0][0] < self.CENTER_X:
                    count_left += 1
                else:
                    count_right += 1
                if name != "Store":
                    count_portal += 1
            if count_portal < 3:
                self.log_queue.put(["还有传送门未识别到", "INF1"])
                if count_left > count_right:
                    press("q")
                    sleep(0.2)
                    return 1
                press("e")
                sleep(0.2)
                return 2
            self.log_queue.put(["所有传送门已识别到", "INF1"])
            return 0

        # 函数主内容
        all_flag = 2  # 标记传送门是否都已显示的变量,0为找到,1为在向左寻找,2为在向右寻找
        prev_all_flag = 0  # 记录上次为找全所有传送门而转动的方向
        # 调整视角以识别到所有传送门的循环
        while True:
            portals = self.detector.infer()
            # 如果一个传送门都未识别到，先转动左右视角找到任意一个传送门
            if not portals:
                self.log_queue.put(["未识别到任何传送门", "INF1"])
                press("e")
                sleep(0.2)
                continue
            log_detection(portals)
            # 如果识别到的传送门是关闭的，先靠近传送门
            if "Lock" in portals:
                press("w")
                sleep(0.2)
                continue
            # 识别到了传送门就调整上下视角以便更好识别传送门
            if justify_perspective(portals) == False:
                continue
            # 如果传送门未全部显示，调整左右视角
            if all_flag != 0:
                all_flag = find_all_portal(portals)
                # 当找全之后,为了避免最后一个找到的门是误判,按照之前的方向多转动一些
                if all_flag == 0:
                    if prev_all_flag == 1:
                        for _ in range(4):
                            press("q")
                            sleep(0.2)
                    elif prev_all_flag == 2:
                        for _ in range(4):
                            press("e")
                            sleep(0.2)
                    # 额外转动后再次判断是否找全
                    sleep(1)
                    all_flag = find_all_portal(portals)
                else:
                    prev_all_flag = all_flag
                continue
            # 运行到此处说明已找到所有传送门且视角调整完毕
            sleep(1)
            # 根据策略选择该层的目标传送门
            names = list(portals.keys())
            target_name = self.strategy.engraving_strategy[
                -1
            ]  # 初始化为优先级最低的刻印
            for name in names:
                # 专属刻印和商店的选择固定在指定层，此处不考虑
                if name == "Elysia" or name == "Store":
                    continue
                if self.strategy.engraving_strategy.index(
                    name
                ) < self.strategy.engraving_strategy.index(target_name):
                    target_name = name
            self.log_queue.put(
                ["本层计划选择[{}]".format(NAME_DICTIONARY[target_name][1]), "INF2"]
            )
            break
        # 向着目标传送门前进
        self.log_queue.put(
            ["开始向[{}]传送门前进".format(NAME_DICTIONARY[target_name][1]), "INF1"]
        )
        while True:
            portals = self.detector.infer()
            log_detection(portals)
            try:
                position = portals[target_name][0]
            # 可能由于移动，人物模型遮挡等原因导致暂时识别不到目标传送门
            except KeyError:
                self.log_queue.put(
                    ["目标[{}]丢失".format(NAME_DICTIONARY[target_name][1]), "WAR"]
                )
                sleep(0.5)
                continue
            # 调整目标传送门到限定的X范围内
            if position[0] < self.TARGET_X_LEFT:
                press("q")
                sleep(0.2)
                continue
            if position[0] > self.TARGET_X_RIGHT:
                press("e")
                sleep(0.2)
                continue
            press("w")
            sleep(1)
            # 激活传送门后退出循环
            if self.ocr.find("传送", region_id=8) is not None:
                sleep(0.5)
                press("r")
                self.log_queue.put(["已到达传送门附近，前往下一层", "INF2"])
                break
        sleep(3)

    def __combat(self, combat_event):
        while not combat_event.is_set():
            # 助战和英桀技能
            press("1")
            press("2")
            press("f")
            sleep(0.2)
            # 女武神操作
            for operation in self.strategy.combat_strategy:
                # hold(长按)类操作
                if operation[0] == "hold":
                    sleep(operation[2])
                    keyDown(operation[1])
                    self.log_queue.put(["按下{}".format(operation[1]), "INF1"])
                    if operation[4] == 0:
                        sleep(5)
                    else:
                        sleep(operation[4])
                    keyUp(operation[1])
                    self.log_queue.put(["抬起{}".format(operation[1]), "INF1"])
                    sleep(operation[3])

    def __combat_validate(self, combat_event):
        while True:
            if self.ocr.find("跳过", region_id=2) is not None:
                combat_event.set()
                self.log_queue.put(["检测到战斗已完成，正在退出战斗线程", "INF1"])
                break
            sleep(1)

    def __normal_layer(self):
        # 前往传送门
        self.__portal()
        # 等待下一层关卡出现
        self.ocr.text("得分", region_id=1)
        combat_event = Event()
        thread_combat = Thread(target=self.__combat, args=(combat_event,), daemon=True)
        thread_validate = Thread(
            target=self.__combat_validate, args=(combat_event,), daemon=True
        )
        thread_combat.start()
        thread_validate.start()
        self.log_queue.put(["启动战斗线程", "INF1"])
        thread_validate.join()
        thread_combat.join()
        self.log_queue.put(["战斗线程已退出", "INF2"])
        # 可能涉及到多次刻印选择(双倍奖励,核心刻印)
        while True:
            # 点击英桀的对话框，进入刻印选择页面
            sleep(1)
            moveTo(self.CENTER_X, self.CENTER_Y)
            sleep(0.2)
            click()
            # 等待选择刻印页面出现
            self.ocr.text("简略", region_id=2)
            sleep(1)
            # 选择核心刻印
            if self.ocr.find("核心", region_id=2) is not None:
                self.__select_core_engraving()
            # 选择一般刻印
            else:
                self.__select_normal_engraving()
            sleep(3)
            # 如果不再有对话框出现,说明刻印已领取完毕
            if self.ocr.find("跳过", region_id=2) is None:
                self.log_queue.put(["本层刻印领取完成", "INF1"])
                break

    def __store_layer(self):
        pass
