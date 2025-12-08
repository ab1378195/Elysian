import tkinter as tk
from tkinter import PhotoImage, filedialog
import ctypes
import os
from controller.procedure import Procedure
from service.accountService import AccountService
from tkinter import messagebox
from model.account import Account
from threading import Thread
from service.strategyService import StrategyService
from service.configurationService import ConfigurationService
from components.widget import Widget

# 常量定义
FREQUENCY_LIST = ["每日一次", "每次启动"]


class APPLICATION:
    def __init__(self, master):
        """程序的GUI界面

        Args:
            master (Tk): tkinter的窗口句柄
        """
        self.master = master
        self.master.title("Elysian")
        self.master.iconbitmap("resources\\ui\\logo.ico")
        self.master["bg"] = "#FFFFFF"
        # 初始化执行线程与遮罩窗口
        self.procedure = Procedure()
        self.procedure_thread = Thread()
        self.set_window_size()
        # 顶部导航栏容器
        self.navbar_frame = tk.Frame(self.master, bg="#FFFFFF", height=50)
        self.navbar_frame.place(x=0, y=0, relwidth=1)
        # 顶部导航栏按钮列表，用于调整按钮激活状态
        self.navbar_buttons = []
        self.create_navbar()
        # 内容部分容器
        self.content_frame = tk.Frame(self.master, bg="#FFFFFF")
        self.content_frame.place(x=0, y=50, relwidth=1, relheight=1)
        # 初始化各个处理业务逻辑的类
        self.confiurationService = ConfigurationService()
        self.accountService = AccountService()
        self.strategyService = StrategyService()
        # 初始化任务清单勾选状态
        self.tasks_list = [tk.IntVar() for _ in range(6)]
        task_configuration = self.confiurationService.get_task_configuration()
        if task_configuration:
            for i, value in enumerate(task_configuration["task"]):
                self.tasks_list[i].set(value)
        # 初始显示启动页
        self.launch_page()

    def set_window_size(self):
        """根据系统DPI设置窗口大小并居中显示"""
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 获取系统DPI缩放
        WIDTH = 800
        HEIGHT = 600
        SCREEN_WIDTH = self.master.winfo_screenwidth()
        SCREEN_HEIGHT = self.master.winfo_screenheight()
        LEFT = (SCREEN_WIDTH - WIDTH) / 2
        TOP = (SCREEN_HEIGHT - HEIGHT) / 2
        self.master.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, LEFT, TOP))
        self.master.minsize(800, 600)

    def create_navbar(self):
        """创建顶部导航栏"""
        navbar_buttons_information = [
            {"text": "一键启动", "command": self.launch_page},
            {"text": "策略配置", "command": self.strategy_page},
            {"text": "软件设置", "command": self.configuration_page},
            {"text": "软件信息", "command": self.information_page},
        ]
        for i, info in enumerate(navbar_buttons_information):
            button = Widget.create_hover_button(
                self.navbar_frame, info["text"], info["command"], relief="raised"
            )
            button.place(relx=0.25 * i, y=0, relwidth=0.25, relheight=1)
            self.navbar_buttons.append(button)

    def destroy_child_widgets(self, master):
        """摧毁master的所有子控件

        Args:
            master (widget): 任意含有子控件的tkinter组件
        """
        for widget in master.winfo_children():
            widget.destroy()

    def clear_content(self, index):
        """清除内容容器的控件并激活对应的导航栏按钮

        Args:
            index (int): 导航栏按钮在列表中的索引
        """
        self.destroy_child_widgets(self.content_frame)
        Widget.set_active_button(index, self.navbar_buttons)

    def clear_canvas(self, canvas, text, index=-1, button_list=[]):
        """清除圆角矩形画布内的控件，更新标题为指定文本，激活对应按钮(可选)

        Args:
            canvas (canvas): 圆角矩形画布
            text (String): 新的标题
            index (int, optional): 要激活的按钮在列表中的索引. Defaults to -1.
            button_list (list, optional): 按钮的列表. Defaults to [].
        """
        self.destroy_child_widgets(canvas)
        tk.Label(
            canvas,
            text=text,
            font=("微软雅黑", 12),
            bg="#FFFFFF",
            fg="#FF9800",
        ).place(relx=0.15, y=5)
        if index != -1 and button_list:
            Widget.set_active_button(index, button_list)

    def launch_page(self):
        """创建一键启动页面"""
        self.clear_content(0)
        # 创建左侧画布用于列出任务清单
        canvas_tasks = Widget.create_round_rectangle_canvas(
            self.content_frame, 10, 20, 10, 10, "#FFA6C3"
        )
        canvas_tasks.place(x=0, y=0, relwidth=0.3, relheight=0.65)

        def configure_material_canvas():
            """创建配置材料活动的画布"""
            self.clear_canvas(canvas_configuration, "材料活动")
            material_label = Widget.create_title_label(canvas_configuration, "材料活动")
            material_label.place(relx=0.4, rely=0.04)
            Widget.create_subtitle_label(canvas_configuration, "执行频率:").place(
                relx=0.05, rely=0.1
            )
            material_frequency = Widget.create_combobox(
                canvas_configuration,
                FREQUENCY_LIST,
                selected_function=lambda e: material_label.focus(),
            )
            material_frequency.place(relx=0.25, rely=0.1, relwidth=0.5, height=30)
            material_configuration = (
                self.confiurationService.get_material_configuration()
            )
            material_frequency.current(
                FREQUENCY_LIST.index(material_configuration["frequency"])
            )

            def save_material_configuration():
                """保存材料活动的配置"""
                self.confiurationService.save_material_configuration(
                    {"frequency": material_frequency.get()}
                )
                messagebox.showinfo(title="提示", message="材料活动配置保存成功")

            Widget.create_success_button(
                canvas_configuration, "Save", save_material_configuration
            ).place(relx=0.8, rely=0.09, relwidth=0.15, relheight=0.07)

        def configure_home_canvas():
            """创建配置家园日常的画布"""
            self.clear_canvas(canvas_configuration, "家园日常")
            # 体力和金币领取的配置部分
            home_reward_label = Widget.create_title_label(
                canvas_configuration, "体力和金币领取"
            )
            home_reward_label.place(relx=0.35, rely=0.04)
            Widget.create_subtitle_label(canvas_configuration, "执行频率:").place(
                relx=0.05, rely=0.1
            )
            home_reward_frequency = Widget.create_combobox(
                canvas_configuration,
                FREQUENCY_LIST,
                selected_function=lambda e: home_reward_label.focus(),
            )
            home_reward_frequency.place(relx=0.25, rely=0.1, relwidth=0.7, height=30)
            # 家园打工的配置部分
            Widget.create_title_label(canvas_configuration, "家园打工").place(
                relx=0.4, rely=0.15
            )
            Widget.create_subtitle_label(canvas_configuration, "执行频率:").place(
                relx=0.05, rely=0.22
            )
            home_quest_frequency = Widget.create_combobox(
                canvas_configuration,
                FREQUENCY_LIST,
                selected_function=lambda e: home_reward_label.focus(),
            )
            home_quest_frequency.place(relx=0.25, rely=0.22, relwidth=0.7, height=30)
            # 家园远征的配置部分
            Widget.create_title_label(canvas_configuration, "家园远征").place(
                relx=0.4, rely=0.29
            )
            Widget.create_subtitle_label(canvas_configuration, "执行频率:").place(
                relx=0.05, rely=0.35
            )
            home_storysweep_frequency = Widget.create_combobox(
                canvas_configuration,
                FREQUENCY_LIST,
                selected_function=lambda e: home_reward_label.focus(),
            )
            home_storysweep_frequency.place(
                relx=0.25, rely=0.35, relwidth=0.7, height=30
            )
            Widget.create_subtitle_label(canvas_configuration, "远征次数:").place(
                relx=0.05, rely=0.42
            )
            home_storysweep_times = Widget.create_entry(
                canvas_configuration, number_validator=True
            )
            home_storysweep_times.place(relx=0.25, rely=0.42, relwidth=0.7, height=30)
            # 加载家园日常的配置
            home_configuration = self.confiurationService.get_home_configuration()
            home_reward_frequency.current(
                FREQUENCY_LIST.index(home_configuration["reward"])
            )
            home_quest_frequency.current(
                FREQUENCY_LIST.index(home_configuration["quest"])
            )
            home_storysweep_frequency.current(
                FREQUENCY_LIST.index(home_configuration["storysweep"][0])
            )
            home_storysweep_times.write(home_configuration["storysweep"][1])

            def save_home_configuration():
                """保存家园日常的配置"""
                if home_storysweep_times.get() == "":
                    messagebox.showerror(title="错误", message="家园远征次数不能为空")
                    return
                self.confiurationService.save_home_configuration(
                    {
                        "reward": home_reward_frequency.get(),
                        "quest": home_quest_frequency.get(),
                        "storysweep": [
                            home_storysweep_frequency.get(),
                            home_storysweep_times.get(),
                        ],
                    }
                )
                messagebox.showinfo(title="提示", message="家园日常的配置保存成功")

            Widget.create_success_button(
                canvas_configuration, "Save", save_home_configuration
            ).place(relx=0.45, rely=0.5, relwidth=0.15, relheight=0.07)

        def configure_commission_canvas():
            """创建配置舰团委托的画布"""
            self.clear_canvas(canvas_configuration, "舰团委托")
            commission_label = Widget.create_title_label(
                canvas_configuration, "舰团委托"
            )
            commission_label.place(relx=0.4, rely=0.04)
            Widget.create_subtitle_label(canvas_configuration, "执行频率:").place(
                relx=0.05, rely=0.1
            )
            commission_frequency = Widget.create_combobox(
                canvas_configuration,
                FREQUENCY_LIST,
                selected_function=lambda e: commission_label.focus(),
            )
            commission_frequency.place(relx=0.25, rely=0.1, relwidth=0.7, height=30)
            Widget.create_subtitle_label(canvas_configuration, "委托次数:").place(
                relx=0.05, rely=0.17
            )
            commission_times = Widget.create_entry(
                canvas_configuration, number_validator=True
            )
            commission_times.place(relx=0.25, rely=0.17, relwidth=0.7, height=30)
            # 加载舰团委托的配置
            commission_configuration = (
                self.confiurationService.get_commission_configuration()
            )
            commission_frequency.current(
                FREQUENCY_LIST.index(commission_configuration["frequency"])
            )
            commission_times.write(commission_configuration["times"])

            def save_commission_configuration():
                """保存舰团委托的相关配置"""
                times = commission_times.get()
                if times == "":
                    messagebox.showerror(title="错误", message="家园远征次数不能为空")
                    return
                if int(times) > 8:
                    messagebox.showerror(title="错误", message="舰团委托次数不能大于8")
                    return
                if times == "0":
                    messagebox.showerror(title="错误", message="舰团委托次数不能为0")
                    return
                self.confiurationService.save_commission_configuration(
                    {"frequency": commission_frequency.get(), "times": times}
                )
                messagebox.showinfo(title="提示", message="舰团委托的配置保存成功")

            Widget.create_success_button(
                canvas_configuration, "Save", save_commission_configuration
            ).place(relx=0.45, rely=0.25, relwidth=0.15, relheight=0.07)

        def cconfigure_shopping_canvas():
            """创建配置每日商店的画布"""
            self.clear_canvas(canvas_configuration, "每日商店")

        def configure_weekly_task_canvas():
            """创建配置周常任务的画布"""
            self.clear_canvas(canvas_configuration, "周常任务")

        def configure_Elysian_canvas():
            """创建配置往世乐土的画布"""
            self.clear_canvas(canvas_configuration, "往世乐土")
            role_label = Widget.create_subtitle_label(canvas_configuration, "角色选择:")
            role_label.place(x=20, rely=0.1)
            strategy_list = self.strategyService.find_all_strategy()
            role_list = {strategy.name_ch: strategy.name for strategy in strategy_list}
            role = Widget.create_combobox(
                canvas_configuration,
                list(role_list.keys()),
                selected_function=lambda e: role_label.focus(),
                placeholder="No role records",
            )
            role.place(x=130, rely=0.1, relwidth=0.65, height=30)
            Widget.create_subtitle_label(canvas_configuration, "难度选择:").place(
                x=20, rely=0.15
            )
            level_list = [
                "终尽(2.75)",
                "侵蚀(2.5)",
                "戒约(2.25)",
                "沦没(2)",
                "劫烧(1.75)",
                "死荫(1.5)",
                "空无(1)",
            ]
            level = Widget.create_combobox(
                canvas_configuration,
                level_list,
                selected_function=lambda e: role_label.focus(),
                placeholder="No level records",
            )
            level.place(x=130, rely=0.16, relwidth=0.65, height=30)
            # 加载往世乐土的配置文件
            Elysian_configuration = self.confiurationService.get_Elysian_configuration()
            role.current(list(role_list.keys()).index(Elysian_configuration["name_ch"]))
            level.current(level_list.index(Elysian_configuration["level"]))

            def save_Elysian_configuration():
                self.confiurationService.save_Elysian_configuration(
                    {
                        "name_ch": role.get(),
                        "level": level.get(),
                        "name": role_list[role.get()],
                    }
                )
                messagebox.showinfo(title="提示", message="配置保存成功")

            Widget.create_success_button(
                canvas_configuration, "Save", save_Elysian_configuration
            ).place(relx=0.45, rely=0.25, relwidth=0.15, relheight=0.07)

        checkbuttons_information = [
            {"text": "材料活动", "command": configure_material_canvas},
            {"text": "家园日常", "command": configure_home_canvas},
            {"text": "舰团委托", "command": configure_commission_canvas},
            {"text": "每日商店", "command": cconfigure_shopping_canvas},
            {"text": "周常任务", "command": configure_weekly_task_canvas},
            {"text": "往世乐土", "command": configure_Elysian_canvas},
        ]
        photo = PhotoImage(file="resources\\ui\\setting.png")
        for i, information in enumerate(checkbuttons_information):
            tk.Checkbutton(
                canvas_tasks,
                text=information["text"],
                bg="#FFFFFF",
                font=("微软雅黑", 12),
                variable=self.tasks_list[i],
            ).place(relx=0.15, rely=0.1 * (i + 1))
            button_rear = tk.Button(
                canvas_tasks,
                image=photo,
                bg="#FFFFFF",
                activebackground="#FFFFFF",
                relief="flat",
                command=information["command"],
            )
            button_rear.image = photo
            button_rear.place(relx=0.7, rely=0.1 * (i + 1) + 0.01)
        # 创建右侧画布用于配置具体任务
        canvas_configuration = Widget.create_round_rectangle_canvas(
            self.content_frame, 10, 20, 10, 60, "#FF9800"
        )
        canvas_configuration.place(relx=0.35, y=0, relwidth=0.65, relheight=1)
        configure_material_canvas()

        def start_perfrom_tasks():
            """启动线程执行已选任务"""
            login_account = self.accountService.get_login_account()
            if login_account is None:
                messagebox.showerror(title="错误", message="尚未选择登录账户")
            elif (
                login_account.channel == "渠道服"
                and not self.confiurationService.get_emulator_configuration()
            ):
                messagebox.showerror(title="错误", message="渠道服账号登录需配置模拟器")
            else:
                tasks_list_int = []
                task_num = 0
                for task in self.tasks_list:
                    tasks_list_int.append(task.get())
                    task_num += task.get()
                if task_num == 0:
                    messagebox.showerror(title="错误", message="尚未选择任何任务")
                elif self.procedure_thread.is_alive() == False:
                    # 保存本次配置的任务清单
                    self.confiurationService.save_task_configuration(
                        {"task": tasks_list_int}
                    )
                    # 启动执行任务的线程
                    self.procedure_thread = Thread(
                        target=self.procedure.perform_tasks,
                        args=(tasks_list_int,),
                        daemon=True,
                    )
                    self.procedure_thread.start()

        Widget.create_normal_button(
            self.content_frame, "启动", start_perfrom_tasks
        ).place(relx=0.1, rely=0.7, relwidth=0.1, relheight=0.1)

    def strategy_page(self):
        """创建策略配置页"""
        self.clear_content(1)
        tk.Label(self.content_frame, text="strategy_page").pack()

    def configuration_page(self):
        """创建软件设置页面"""
        self.clear_content(2)
        # 创建左侧画布用于展示可修改设置列表
        canvas_settings = Widget.create_round_rectangle_canvas(
            self.content_frame, 10, 20, 10, 60, "#FFA6C3"
        )
        canvas_settings.place(x=0, y=0, relwidth=0.2, relheight=1)

        def configure_account_canvas():
            """创建配置账户的画布"""
            self.clear_canvas(
                canvas_configuration,
                "账户设置",
                index=0,
                button_list=configuration_buttons,
            )
            # 选择登录账户的部分
            Widget.create_title_label(canvas_configuration, "登录账户").place(
                relx=0.45, y=40
            )
            Widget.create_subtitle_label(canvas_configuration, "uid:").place(
                relx=0.05, rely=0.15
            )
            account_list = self.accountService.find_all_account()
            uid_list = [account.uid for account in account_list]

            def login_uid_selected(event):
                """选择了uid后展示对应account的信息

                Args:
                    event (event): 触发事件
                """
                uid = login_uid.get()
                for account in account_list:
                    if account.uid == uid:
                        show_account_detail(account)
                        break
                # 聚焦于别的组件以消除选择框
                login_account.focus()

            login_uid = Widget.create_combobox(
                canvas_configuration,
                uid_list,
                selected_function=login_uid_selected,
                placeholder="No login records",
            )
            login_uid.place(relx=0.14, rely=0.15, relwidth=0.3, height=30)
            Widget.create_subtitle_label(canvas_configuration, "渠道:").place(
                relx=0.55, rely=0.15
            )
            login_channel = Widget.create_entry(canvas_configuration, state="readonly")
            login_channel.place(relx=0.65, rely=0.15, relwidth=0.3, height=30)
            Widget.create_subtitle_label(canvas_configuration, "账户:").place(
                relx=0.05, rely=0.25
            )
            login_account = Widget.create_entry(canvas_configuration, state="readonly")
            login_account.place(relx=0.14, rely=0.25, relwidth=0.3, height=30)
            Widget.create_subtitle_label(canvas_configuration, "密码:").place(
                relx=0.55, rely=0.25
            )
            login_password = Widget.create_entry(canvas_configuration, state="readonly")
            login_password.place(relx=0.65, rely=0.25, relwidth=0.3, height=30)

            def show_account_detail(account):
                """显示账户的详细信息

                Args:
                    account (Account): 要显示信息的account
                """
                login_channel.write(account.channel)
                login_account.write(account.account)
                login_password.write(account.password)

            # 显示之前配置的登录账户
            prev_login_account = self.accountService.get_login_account()
            if prev_login_account is not None:
                login_uid.current(account_list.index(prev_login_account))
                show_account_detail(prev_login_account)

            def save_login_account():
                """保存登录账户"""
                self.accountService.update_login_account(login_uid.get())
                messagebox.showinfo(title="提示", message="新登录账户保存成功")

            Widget.create_success_button(
                canvas_configuration, "Save", save_login_account
            ).place(relx=0.28, rely=0.32, relwidth=0.15, relheight=0.07)

            def delete_account():
                """删除选中的账户"""
                self.accountService.delete(login_uid.get())
                configure_account_canvas()
                messagebox.showinfo(title="提示", message="账户已成功删除")

            Widget.create_danger_button(
                canvas_configuration, "Delete", delete_account
            ).place(relx=0.6, rely=0.32, relwidth=0.15, relheight=0.07)
            # 创建账户的部分
            Widget.create_title_label(canvas_configuration, "创建账户").place(
                relx=0.45, rely=0.4
            )
            Widget.create_subtitle_label(canvas_configuration, "uid:").place(
                relx=0.05, rely=0.5
            )

            new_uid = Widget.create_entry(canvas_configuration, number_validator=True)
            new_uid.place(relx=0.14, rely=0.5, relwidth=0.3, height=30)
            Widget.create_subtitle_label(canvas_configuration, "渠道:").place(
                relx=0.55, rely=0.5
            )
            new_channel = Widget.create_combobox(
                canvas_configuration,
                ["官服", "Android", "ios", "渠道服"],
                selected_function=lambda e: login_account.focus(),
            )
            new_channel.place(relx=0.65, rely=0.5, relwidth=0.3, height=30)
            Widget.create_subtitle_label(canvas_configuration, "账户:").place(
                relx=0.05, rely=0.6
            )
            new_account = Widget.create_entry(
                canvas_configuration, number_validator=True
            )
            new_account.place(relx=0.14, rely=0.6, relwidth=0.3, height=30)
            Widget.create_subtitle_label(canvas_configuration, "密码:").place(
                relx=0.55, rely=0.6
            )
            new_password = Widget.create_entry(canvas_configuration)
            new_password.place(relx=0.65, rely=0.6, relwidth=0.3, height=30)

            def create_new_account():
                """验证账户是否已存在，不存在则创建新账户"""
                account = Account()
                account.account = new_account.get()
                account.channel = new_channel.get()
                account.password = new_password.get().strip()
                account.uid = new_uid.get().strip()
                account.login = 0
                if account.uid == "":
                    messagebox.showerror(title="错误", message="uid尚未填写")
                    return
                if account.channel != "渠道服":
                    if account.account == "":
                        messagebox.showerror(title="错误", message="账户尚未填写")
                        return
                    if account.password == "":
                        messagebox.showerror(title="错误", message="密码尚未填写")
                        return
                if account in account_list:
                    messagebox.showerror(title="错误", message="该账户已存在")
                    return
                self.accountService.save(account)
                configure_account_canvas()
                messagebox.showinfo(title="提示", message="新账户创建成功")

            Widget.create_success_button(
                canvas_configuration, "Create", create_new_account
            ).place(relx=0.43, rely=0.7, relwidth=0.15, relheight=0.07)

        def configure_update_canvas():
            """创建配置更新设置的画布"""
            self.clear_canvas(
                canvas_configuration,
                "更新设置",
                index=1,
                button_list=configuration_buttons,
            )

        def configure_hotkey_canvas():
            """创建配置热键的画布"""
            self.clear_canvas(
                canvas_configuration,
                "热键设置",
                index=2,
                button_list=configuration_buttons,
            )

        def configure_emulator_canvas():
            """创建配置模拟器的画布"""
            self.clear_canvas(
                canvas_configuration,
                "模拟器设置",
                index=3,
                button_list=configuration_buttons,
            )
            Widget.create_title_label(canvas_configuration, "模拟器路径").place(
                relx=0.42, rely=0.08
            )
            emulator = Widget.create_entry(canvas_configuration, state="readonly")
            emulator.place(relx=0.05, rely=0.15, relwidth=0.7, height=30)

            def browse_emulator():
                """浏览文件选择模拟器路径"""
                emulator_path = filedialog.askopenfilename(
                    title="请选择模拟器路径",
                    filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")],
                )
                if emulator_path:
                    emulator.write(emulator_path)

            Widget.create_success_button(
                canvas_configuration, "Browse", browse_emulator
            ).place(relx=0.8, rely=0.13, relwidth=0.15, height=50)
            Widget.create_subtitle_label(canvas_configuration, "模拟器编号:").place(
                relx=0.05, rely=0.24
            )
            index = Widget.create_entry(canvas_configuration, number_validator=True)
            index.place(relx=0.25, rely=0.25, relwidth=0.6, height=30)

            def save_emulator_configuration():
                """保存模拟器配置信息"""
                path = emulator.get()
                if path == "No path configuration information":
                    messagebox.showerror(title="错误", message="尚未选择模拟器路径")
                    return
                if index.get() == "":
                    messagebox.showerror(title="错误", message="尚未设置模拟器编号")
                    return
                self.confiurationService.save_emulator_configuration(
                    {"path": path, "index": int(index.get())}
                )
                messagebox.showinfo(title="提示", message="模拟器配置保存成功")

            Widget.create_success_button(
                canvas_configuration, "Save", save_emulator_configuration
            ).place(relx=0.43, rely=0.32, relwidth=0.15, height=40)
            # 显示之前的模拟器配置信息
            emulator_configuration = (
                self.confiurationService.get_emulator_configuration()
            )
            if emulator_configuration:
                emulator.write(emulator_configuration["path"])
                index.write(emulator_configuration["index"])
            else:
                emulator.write("No path configuration information")

        btn_configs_info = [
            {"text": "账户设置", "command": configure_account_canvas},
            {"text": "更新设置", "command": configure_update_canvas},
            {"text": "热键设置", "command": configure_hotkey_canvas},
            {"text": "模拟器设置", "command": configure_emulator_canvas},
        ]
        configuration_buttons = []
        for i, info in enumerate(btn_configs_info):
            btn = Widget.create_hover_button(
                canvas_settings, info["text"], info["command"]
            )
            btn.place(relx=0.1, y=25 + 30 * i, relwidth=0.8, height=30)
            configuration_buttons.append(btn)
        # 创建右侧画布用于配置具体设置项
        canvas_configuration = Widget.create_round_rectangle_canvas(
            self.content_frame, 10, 20, 10, 60, "#FF9800"
        )
        canvas_configuration.place(relx=0.25, y=0, relwidth=0.75, relheight=1)
        configure_account_canvas()

    def information_page(self):
        """创建软件信息页面"""
        self.clear_content(3)
        tk.Label(self.content_frame, text="information_page").pack()


def on_closing(window):
    """GUI的关闭函数，使GUI关闭时，所有进程终止

    Args:
        window (Tk): tkinter窗口句柄
    """
    window.quit()
    window.destroy()
    os._exit(0)


def GUI():
    """启动GUI"""
    Elysian = tk.Tk()
    application = APPLICATION(Elysian)
    Elysian.protocol("WM_DELETE_WINDOW", lambda: on_closing(Elysian))
    Elysian.mainloop()
