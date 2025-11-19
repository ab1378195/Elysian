import tkinter as tk
from tkinter import PhotoImage, filedialog
from tkinter.ttk import Combobox
import ctypes
import os
from controller.procedure import Procedure
from service.accountService import AccountService
from tkinter import messagebox
from model.account import Account
from threading import Thread
from service.strategyService import StrategyService


class APPLICATION:
    """the GUI for user to interact with the program"""

    def __init__(self, master):
        """the basic attributes for GUI and the initilization

        Args:
            master (tkinter.Tk()): the window handling
        """
        self.master = master
        self.master.title("Elysian")
        self.master.iconbitmap("resources\\ui\\logo.ico")
        self.master["bg"] = "#FFFFFF"
        self.tasks_list = [tk.IntVar() for _ in range(6)]
        self.procedure = Procedure()
        self.procedure_thread = Thread()
        # encapsulate the validation function to be used in other widget
        self.validator_number = self.master.register(self.validate_number_input)
        self.create_navbar()
        self.create_content()
        self.set_window_size()

    def set_window_size(self):
        """set window size and make it appear in the center of the screen"""
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # get system's DPI
        WIDTH = 800
        HEIGHT = 600
        SCREEN_WIDTH = self.master.winfo_screenwidth()
        SCREEN_HEIGHT = self.master.winfo_screenheight()
        LEFT = (SCREEN_WIDTH - WIDTH) / 2
        TOP = (SCREEN_HEIGHT - HEIGHT) / 2
        self.master.geometry("%dx%d+%d+%d" % (WIDTH, HEIGHT, LEFT, TOP))
        self.master.minsize(800, 600)

    def hoverEffect(self, button, leave_bg="#FFFFFF"):
        """add hover effect for the button

        Args:
            button (tkinter.Button): the button needs to add hover effect
            leave_bg (str, optional): the color when the mouse leaves the button. Defaults to "#FFFFFF".
        """

        def on_enter(event):
            """the effect when mouse hovers the button

            Args:
                event (event): the tkinter event
            """
            if button["fg"] != "#FF9800":
                button["bg"] = "#FCE4EC"
                button["fg"] = "#E91E63"

        def on_leave(event):
            """the effect when mouse leaves the button

            Args:
                event (event): the tkinter event
            """
            if button["fg"] != "#FF9800":
                button["bg"] = leave_bg
                button["fg"] = "#000000"

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def create_navbar(self):
        """create navbar"""
        # navbar container
        self.navbar = tk.Frame(self.master, bg="#FFFFFF", height=50)
        self.navbar.place(x=0, y=0, relwidth=1)
        # button style
        self.button_style = {
            "bg": "#E3E4E5",
            "fg": "#000000",
            "font": ("微软雅黑", 12),
            "activebackground": "#FFF8E1",
            "activeforeground": "#FF9800",
        }
        # navbar button list, for justify actived button style
        self.navbar_buttons = []
        # button information
        navbar_buttons_information = [
            {"text": "一键启动", "command": self.launch_page},
            {"text": "策略配置", "command": self.strategy_page},
            {"text": "软件设置", "command": self.config_page},
            {"text": "软件信息", "command": self.information_page},
        ]
        # add button
        for i, item in enumerate(navbar_buttons_information):
            btn = tk.Button(
                self.navbar,
                text=item["text"],
                command=item["command"],
                **self.button_style
            )
            btn.place(relx=0.25 * i, y=0, relwidth=0.25, relheight=1)
            self.navbar_buttons.append(btn)
            self.hoverEffect(btn, "#E3E4E5")

    def clear_content(self):
        """destroy all widgets in content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def set_active_button(self, index, btn_list, default_bg="#FFFFFF"):
        """justify the targeted button to active style and justify other buttons in list back to normal style

        Args:
            index (int): the button index in the button list
            btn_list (List<tkinter.button>): a list contains several buttons
            default_bg (str, optional): the background color of normal button style. Defaults to "#FFFFFF".
        """
        for i, btn in enumerate(btn_list):
            if i == index:
                btn["bg"] = "#FFF8E1"
                btn["fg"] = "#FF9800"
            else:
                btn["bg"] = default_bg
                btn["fg"] = "#000000"

    def create_content(self):
        """create a frame as content container"""
        # content container
        self.content_frame = tk.Frame(self.master, bg="#FFFFFF")
        self.content_frame.place(x=0, y=50, relwidth=1, relheight=1)
        self.launch_page()

    def update_rectangle(
        self, event, widget, x1_gap, y1_gap, x2_gap, y2_gap, radius=25, **kwargs
    ):
        """draw a rectangle for the widget

        Args:
            event (event): the event to trigger this function
            widget (tkinter.contoller): the widget needs to draw a rectangle
            x1_gap (int): the x-distance of left-top point and widget's left boundary
            y1_gap (int): the y-distance of left-top point and widget's top boundary
            x2_gap (int): the x-distance of right-bottom point and widget's right boundary
            y2_gap (int): the y-distance of right-bottom point and widget's bottom boundary
            radius (int, optional): the radius of the rectangle. Defaults to 25.
        """
        if widget.rect_id is not None:
            widget.delete(widget.rect_id)
        width = widget.winfo_width()
        height = widget.winfo_height()
        x1 = x1_gap
        x2 = width - x2_gap
        y1 = y1_gap
        y2 = height - y2_gap
        points = [
            x1 + radius,
            y1,
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]
        widget.rect_id = widget.create_polygon(points, **kwargs, smooth=True)

    def validate_number_input(self, text):
        """validate the text, only return true when the text is digit or empty

        Args:
            text (String): the text be validated

        Returns:
            boolean: whether the text is digit (empty) or not
        """
        return text.isdigit() or text == ""

    def launch_page(self):
        """create launch page"""
        self.clear_content()
        self.set_active_button(0, self.navbar_buttons, default_bg="#E3E4E5")
        # create the left canvas for displaying tasks list
        canvas_tasks = tk.Canvas(self.content_frame, bg="#FFFFFF", highlightthickness=0)
        canvas_tasks.place(x=0, y=0, relwidth=0.3, relheight=0.65)
        canvas_tasks.rect_id = None
        canvas_tasks.bind(
            "<Configure>",
            lambda event: self.update_rectangle(
                event,
                canvas_tasks,
                10,
                20,
                10,
                10,
                fill="#FFFFFF",
                outline="#FFA6C3",
                width=1,
            ),
        )

        def clear_canvas_setting(text):
            """destroy all widgets in the setting canvas and display the title of the setting canvas

            Args:
                text (String): the title of the setting canvas
            """
            for widget in canvas_setting.winfo_children():
                widget.destroy()
            tk.Label(
                canvas_setting,
                text=text,
                font=("微软雅黑", 12),
                bg="#FFFFFF",
                fg="#FF9800",
            ).place(relx=0.15, y=5)

        def create_configure_working():
            """create the working configuration canvas"""
            clear_canvas_setting("家园打工")

        def create_configure_Expedition():
            """create the expedition configuration canvas"""
            clear_canvas_setting("远征派遣")

        def create_configure_commission():
            """create the commission configuration canvas"""
            clear_canvas_setting("舰团委托")

        def create_configure_shopping():
            """create the shopping configuration canvas"""
            clear_canvas_setting("每日商店")

        def create_configure_weekly_task():
            """create the weekly task configuration canvas"""
            clear_canvas_setting("周常任务")

        def create_configure_Elysian():
            """create the Elysian configuration canvas"""
            clear_canvas_setting("往世乐土")
            strategyService = StrategyService()
            role_label = tk.Label(
                canvas_setting,
                text="角色选择:",
                font=("微软雅黑", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            )
            role_label.place(x=20, rely=0.1)
            strategy_list = strategyService.findAll()
            role_list = [strategy.name_ch for strategy in strategy_list]
            role = Combobox(
                canvas_setting,
                values=role_list,
                justify="center",
                font=("微软雅黑", 12),
                state="readonly",
            )
            role.place(x=130, rely=0.1, relwidth=0.65, height=30)
            role.bind("<<ComboboxSelected>>", lambda e: role_label.focus())
            tk.Label(
                canvas_setting,
                text="难度选择:",
                font=("微软雅黑", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            ).place(x=20, rely=0.15)
            level_list = [
                "终尽(2.75)",
                "侵蚀(2.5)",
                "戒约(2.25)",
                "沦没(2)",
                "劫烧(1.75)",
                "死荫(1.5)",
                "空无(1)",
            ]
            level = Combobox(
                canvas_setting,
                values=level_list,
                justify="center",
                font=("微软雅黑", 12),
                state="readonly",
            )
            level.place(x=130, rely=0.16, relwidth=0.65, height=30)
            level.bind("<<ComboboxSelected>>", lambda e: role_label.focus())
            config_info = strategyService.getConfig()
            role.current(role_list.index(config_info["name_ch"]))
            level.current(level_list.index(config_info["level"]))

            def save_config():
                strategyService.saveConfig(
                    {"name_ch": role.get(), "level": level.get()}
                )
                messagebox.showinfo(title="提示", message="配置保存成功")

            tk.Button(
                canvas_setting,
                text="Save",
                font=("Arial", 14, "bold"),
                bg="#1CCD6F",
                fg="#FFFFFF",
                activebackground="#1CC4CD",
                activeforeground="#FFFFFF",
                bd=0,
                relief="flat",
                cursor="hand2",
                highlightbackground="#DAA520",
                highlightthickness=1,
                command=save_config,
            ).place(relx=0.45, rely=0.25, relwidth=0.15, relheight=0.07)

        checkbuttons_information = [
            {"text": "家园打工", "command": create_configure_working},
            {"text": "远征派遣", "command": create_configure_Expedition},
            {"text": "舰团委托", "command": create_configure_commission},
            {"text": "每日商店", "command": create_configure_shopping},
            {"text": "周常任务", "command": create_configure_weekly_task},
            {"text": "往世乐土", "command": create_configure_Elysian},
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
        # create the right canvas for configuring a task
        canvas_setting = tk.Canvas(
            self.content_frame, bg="#FFFFFF", highlightthickness=0
        )
        canvas_setting.place(relx=0.35, y=0, relwidth=0.65, relheight=1)
        canvas_setting.rect_id = None
        canvas_setting.bind(
            "<Configure>",
            lambda event: self.update_rectangle(
                event,
                canvas_setting,
                10,
                20,
                10,
                60,
                fill="#FFFFFF",
                outline="#FF9800",
                width=1,
            ),
        )
        create_configure_working()

        def start_perfrom_tasks():
            """start a thread to perform the selected task"""
            accountService = AccountService()
            login_account = accountService.get_login_account()
            if login_account is None:
                messagebox.showerror(title="错误", message="尚未选择登录账户")
            elif login_account.channel == "渠道服" and not accountService.get_emulator_config():
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
                    self.procedure_thread = Thread(
                        target=self.procedure.perform_tasks,
                        args=(tasks_list_int,),
                        daemon=True,
                    )
                    self.procedure_thread.start()

        tk.Button(
            self.content_frame,
            text="启动",
            font=("微软雅黑", 14, "bold"),
            bg="#FFB6C1",
            fg="#8B4513",
            activebackground="#FF69B4",
            activeforeground="#FFFFFF",
            bd=0,
            relief="flat",
            cursor="hand2",
            highlightbackground="#DAA520",
            highlightthickness=1,
            command=start_perfrom_tasks,
        ).place(relx=0.1, rely=0.7, relwidth=0.1, relheight=0.1)

    def strategy_page(self):
        """create strategy page"""
        self.clear_content()
        self.set_active_button(1, self.navbar_buttons, default_bg="#E3E4E5")
        tk.Label(self.content_frame, text="strategy_page").pack()

    def config_page(self):
        """create config page"""
        self.clear_content()
        self.set_active_button(2, self.navbar_buttons, default_bg="#E3E4E5")
        # create the left canvas for displaying program configs
        canvas_configs = tk.Canvas(
            self.content_frame, bg="#FFFFFF", highlightthickness=0
        )
        canvas_configs.place(x=0, y=0, relwidth=0.2, relheight=1)
        canvas_configs.rect_id = None
        canvas_configs.bind(
            "<Configure>",
            lambda event: self.update_rectangle(
                event,
                canvas_configs,
                10,
                20,
                10,
                60,
                fill="#FFFFFF",
                outline="#FFA6C3",
                width=1,
            ),
        )

        def clear_canvas_configuration(text):
            """destroy all widgets in configuration canvas (right) and show the title of the configuration canvas

            Args:
                text (String): the title of the configuration canvas
            """
            for widget in canvas_setting.winfo_children():
                widget.destroy()
            tk.Label(
                canvas_setting,
                text=text,
                font=("微软雅黑", 12),
                bg="#FFFFFF",
                fg="#FF9800",
            ).place(relx=0.15, y=5)

        def configure_account():
            """create the account configuration canvas"""
            clear_canvas_configuration("账户设置")
            self.set_active_button(0, config_btns)
            accountService = AccountService()
            # the login account selected section
            tk.Label(
                canvas_setting,
                text="登录账户",
                font=("微软雅黑", 14, "bold"),
                bg="#FFFFFF",
                fg="#E91E63",
            ).place(relx=0.45, y=40)
            tk.Label(
                canvas_setting,
                text="uid:",
                font=("Arial", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            ).place(relx=0.05, rely=0.15)
            account_list = accountService.findAll()
            uid_list = [account.uid for account in account_list]
            login_uid = Combobox(
                canvas_setting,
                values=uid_list,
                justify="center",
                font=("Arial", 12),
                state="readonly",
            )
            login_uid.place(relx=0.14, rely=0.15, relwidth=0.3, height=30)
            login_uid.set("No login records")
            tk.Label(
                canvas_setting,
                text="渠道:",
                font=("微软雅黑", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            ).place(relx=0.55, rely=0.15)
            login_channel = tk.Entry(
                canvas_setting,
                font=("微软雅黑", 12),
                justify="center",
                relief="solid",
                state="readonly",
            )
            login_channel.place(relx=0.65, rely=0.15, relwidth=0.3, height=30)
            tk.Label(
                canvas_setting,
                text="账户:",
                font=("微软雅黑", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            ).place(relx=0.05, rely=0.25)
            login_account = tk.Entry(
                canvas_setting,
                font=("Arial", 12),
                justify="center",
                relief="solid",
                state="readonly",
            )
            login_account.place(relx=0.14, rely=0.25, relwidth=0.3, height=30)
            tk.Label(
                canvas_setting,
                text="密码:",
                font=("微软雅黑", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            ).place(relx=0.55, rely=0.25)
            login_password = tk.Entry(
                canvas_setting,
                font=("Arial", 12),
                justify="center",
                relief="solid",
                state="readonly",
            )
            login_password.place(relx=0.65, rely=0.25, relwidth=0.3, height=30)

            def show_account_detail(account):
                """show the detail of the account

                Args:
                    account (Account): the account needs to be displayed
                """
                login_channel["state"] = "normal"
                login_channel.delete(0, tk.END)
                login_account["state"] = "normal"
                login_account.delete(0, tk.END)
                login_password["state"] = "normal"
                login_password.delete(0, tk.END)
                login_channel.insert(0, account.channel)
                login_account.insert(0, account.account)
                login_password.insert(0, account.password)
                login_channel["state"] = "readonly"
                login_account["state"] = "readonly"
                login_password["state"] = "readonly"

            def login_uid_selected(event):
                """show account's detail of the selected uid

                Args:
                    event (event): the event to trigger the function
                """
                uid = login_uid.get()
                for account in account_list:
                    if account.uid == uid:
                        show_account_detail(account)
                        break
                # focus on another widget to avoid blue background after selection
                login_account.focus()

            login_uid.bind("<<ComboboxSelected>>", login_uid_selected)
            # find the login account and show its detail
            for i, account in enumerate(account_list):
                if account.login == 1:
                    login_uid.current(i)
                    show_account_detail(account)
                    break

            def save_login_account():
                """save the login account"""
                accountService.update_login_account(login_uid.get())
                messagebox.showinfo(title="提示", message="新登录账户保存成功")

            tk.Button(
                canvas_setting,
                text="Save",
                font=("Arial", 14, "bold"),
                bg="#1CCD6F",
                fg="#FFFFFF",
                activebackground="#1CC4CD",
                activeforeground="#FFFFFF",
                bd=0,
                relief="flat",
                cursor="hand2",
                highlightbackground="#DAA520",
                highlightthickness=1,
                command=save_login_account,
            ).place(relx=0.28, rely=0.32, relwidth=0.15, relheight=0.07)

            def delete_account():
                """delete the selected account"""
                accountService.delete(login_uid.get())
                configure_account()
                messagebox.showinfo(title="提示", message="账户已成功删除")

            tk.Button(
                canvas_setting,
                text="Delete",
                font=("Arial", 14, "bold"),
                bg="#CD691C",
                fg="#FFFFFF",
                activebackground="#CD1C37",
                activeforeground="#FFFFFF",
                bd=0,
                relief="flat",
                cursor="hand2",
                highlightbackground="#DAA520",
                highlightthickness=1,
                command=delete_account,
            ).place(relx=0.6, rely=0.32, relwidth=0.15, relheight=0.07)
            # the section of creating a new account
            tk.Label(
                canvas_setting,
                text="创建账户",
                font=("微软雅黑", 14, "bold"),
                bg="#FFFFFF",
                fg="#E91E63",
            ).place(relx=0.45, rely=0.4)
            tk.Label(
                canvas_setting,
                text="uid:",
                font=("Arial", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            ).place(relx=0.05, rely=0.5)

            new_uid = tk.Entry(
                canvas_setting,
                justify="center",
                font=("Arial", 12),
                relief="solid",
                validate="key",
                validatecommand=(self.validator_number, "%P"),
            )
            new_uid.place(relx=0.14, rely=0.5, relwidth=0.3, height=30)
            tk.Label(
                canvas_setting,
                text="渠道:",
                font=("微软雅黑", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            ).place(relx=0.55, rely=0.5)
            new_channel = Combobox(
                canvas_setting,
                font=("微软雅黑", 12),
                justify="center",
                state="readonly",
                values=["官服", "Android", "ios", "渠道服"],
            )
            new_channel.place(relx=0.65, rely=0.5, relwidth=0.3, height=30)
            new_channel.bind("<<ComboboxSelected>>", lambda e: login_account.focus())
            tk.Label(
                canvas_setting,
                text="账户:",
                font=("微软雅黑", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            ).place(relx=0.05, rely=0.6)
            new_account = tk.Entry(
                canvas_setting,
                font=("Arial", 12),
                justify="center",
                relief="solid",
                validate="key",
                validatecommand=(self.validator_number, "%P"),
            )
            new_account.place(relx=0.14, rely=0.6, relwidth=0.3, height=30)
            tk.Label(
                canvas_setting,
                text="密码:",
                font=("微软雅黑", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            ).place(relx=0.55, rely=0.6)
            new_password = tk.Entry(
                canvas_setting, font=("Arial", 12), justify="center", relief="solid"
            )
            new_password.place(relx=0.65, rely=0.6, relwidth=0.3, height=30)

            def create_new_account():
                """validate whether the account is already existing, if not, create a new account"""
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
                accountService.save(account)
                configure_account()
                messagebox.showinfo(title="提示", message="新账户创建成功")

            tk.Button(
                canvas_setting,
                text="Create",
                font=("Arial", 14, "bold"),
                bg="#1CCD6F",
                fg="#FFFFFF",
                activebackground="#1CC4CD",
                activeforeground="#FFFFFF",
                bd=0,
                relief="flat",
                cursor="hand2",
                highlightbackground="#DAA520",
                highlightthickness=1,
                command=create_new_account,
            ).place(relx=0.43, rely=0.7, relwidth=0.15, relheight=0.07)

        def configure_update():
            """create the update configuration canvas"""
            clear_canvas_configuration("更新设置")
            self.set_active_button(1, config_btns)

        def configure_hotkey():
            """create the hotkey configuration canvas"""
            clear_canvas_configuration("热键设置")
            self.set_active_button(2, config_btns)

        def configure_emulator():
            clear_canvas_configuration("模拟器设置")
            self.set_active_button(3, config_btns)
            tk.Label(
                canvas_setting,
                text="模拟器路径",
                font=("微软雅黑", 12, "bold"),
                bg="#FFFFFF",
                fg="#E91E63",
            ).place(relx=0.42, rely=0.08)
            emulator = tk.Entry(
                canvas_setting,
                font=("Arial", 12),
                bg="#FFFFFF",
                fg="#000000",
                relief="solid",
                state="readonly",
                justify="center",
            )
            emulator.place(relx=0.05, rely=0.15, relwidth=0.7, height=30)

            def browse_emulator():
                emulator_path = filedialog.askopenfilename(
                    title="请选择模拟器路径",
                    filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")],
                )
                if emulator_path:
                    emulator["state"] = "normal"
                    emulator.delete(0, tk.END)
                    emulator.insert(0, emulator_path)
                    emulator["state"] = "readonly"

            tk.Button(
                canvas_setting,
                text="Browse",
                font=("Arial", 12, "bold"),
                bg="#1CCD6F",
                fg="#FFFFFF",
                activebackground="#1CC4CD",
                activeforeground="#FFFFFF",
                bd=0,
                relief="flat",
                cursor="hand2",
                highlightbackground="#DAA520",
                highlightthickness=1,
                command=browse_emulator,
            ).place(relx=0.8, rely=0.13, relwidth=0.15, height=50)
            tk.Label(
                canvas_setting,
                text="模拟器编号:",
                font=("微软雅黑", 12, "bold"),
                bg="#FFFFFF",
                fg="#FFA6C3",
            ).place(relx=0.05, rely=0.24)
            index = tk.Entry(
                canvas_setting,
                font=("Arial", 12),
                bg="#FFFFFF",
                fg="#000000",
                relief="solid",
                justify="center",
                validate="key",
                validatecommand=(self.validator_number, "%P"),
            )
            index.place(relx=0.25, rely=0.25, relwidth=0.6, height=30)
            

            def save_emulator_config():
                path = emulator.get()
                if path == "No path configuration information":
                    messagebox.showerror(title="错误",message="尚未选择模拟器路径")
                    return
                if index.get()=="":
                    messagebox.showerror(title="错误",message="尚未设置模拟器编号")
                    return
                accountService.save_emulator_config(
                    {"path": path, "index": int(index.get())}
                )
                messagebox.showinfo(title="提示", message="模拟器配置保存成功")

            tk.Button(
                canvas_setting,
                text="Save",
                font=("Arial", 12, "bold"),
                bg="#1CCD6F",
                fg="#FFFFFF",
                activebackground="#1CC4CD",
                activeforeground="#FFFFFF",
                bd=0,
                relief="flat",
                cursor="hand2",
                highlightbackground="#DAA520",
                highlightthickness=1,
                command=save_emulator_config,
            ).place(relx=0.43, rely=0.32, relwidth=0.15, height=40)
            # load emulator config
            accountService = AccountService()
            emulator_info = accountService.get_emulator_config()
            emulator["state"] = "normal"
            emulator.delete(0, tk.END)
            index.delete(0, tk.END)
            if emulator_info:
                emulator.insert(0, emulator_info["path"])
                index.insert(0, emulator_info["index"])
            else:
                emulator.insert(0, "No path configuration information")
            emulator["state"] = "readonly"

        btn_configs_info = [
            {"text": "账户设置", "command": configure_account},
            {"text": "更新设置", "command": configure_update},
            {"text": "热键设置", "command": configure_hotkey},
            {"text": "模拟器设置", "command": configure_emulator},
        ]
        config_btns = []
        for i, info in enumerate(btn_configs_info):
            btn = tk.Button(
                canvas_configs,
                text=info["text"],
                font=("微软雅黑", 12),
                bg="#FFFFFF",
                fg="#000000",
                activebackground="#FFF8E1",
                activeforeground="#FF9800",
                relief="flat",
                command=info["command"],
            )
            btn.place(relx=0.1, y=25 + 30 * i, relwidth=0.8, height=30)
            self.hoverEffect(btn)
            config_btns.append(btn)
        # create the right canvas for configuring the program setting
        canvas_setting = tk.Canvas(
            self.content_frame, bg="#FFFFFF", highlightthickness=0
        )
        canvas_setting.place(relx=0.25, y=0, relwidth=0.75, relheight=1)
        canvas_setting.rect_id = None
        canvas_setting.bind(
            "<Configure>",
            lambda event: self.update_rectangle(
                event,
                canvas_setting,
                10,
                20,
                10,
                60,
                fill="#FFFFFF",
                outline="#FF9800",
                width=1,
            ),
        )
        configure_account()

    def information_page(self):
        """create information page"""
        self.clear_content()
        self.set_active_button(3, self.navbar_buttons, default_bg="#E3E4E5")
        tk.Label(self.content_frame, text="information_page").pack()


def on_closing(window):
    """the closing function for the GUI, ensure all process are terminated

    Args:
        window (tkinter.Tk): the window handling
    """
    window.quit()
    window.destroy()
    os._exit(0)


def GUI():
    """boot a GUI application"""
    Elysian = tk.Tk()
    application = APPLICATION(Elysian)
    Elysian.protocol("WM_DELETE_WINDOW", lambda: on_closing(Elysian))
    Elysian.mainloop()
