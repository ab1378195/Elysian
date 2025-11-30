import tkinter as tk
from tkinter.ttk import Combobox


class Widget:
    @staticmethod
    def create_title_label(master, text):
        """创建title级label(红色)

        Args:
            master (widget): 父组件
            text (String): 标签文本

        Returns:
            Label: 创建的label
        """
        return tk.Label(
            master,
            text=text,
            font=("微软雅黑", 14, "bold"),
            bg="#FFFFFF",
            fg="#E91E63",
        )

    @staticmethod
    def create_subtitle_label(master, text):
        """创建子标题级label(粉色)

        Args:
            master (widget): 父组件
            text (String): 标签文本

        Returns:
            Label: 创建的label
        """
        return tk.Label(
            master,
            text=text,
            font=("微软雅黑", 12, "bold"),
            bg="#FFFFFF",
            fg="#FFA6C3",
        )

    @staticmethod
    def create_hover_button(master, text, command, relief="flat"):
        """创建有hover响应的按钮

        Args:
            master (widget): 父组件
            text (String): 按钮文本
            command (function): 按钮函数
            relief (str, optional): 按钮浮雕样式. Defaults to "flat".
        """

        def hoverEffect(button):
            """为按钮添加hover响应

            Args:
                button (Button): 需要添加hover响应的按钮
            """

            def on_enter(event):
                """添加鼠标移入响应

                Args:
                    event (event): 触发事件
                """
                if button["fg"] != "#FF9800":
                    button["bg"] = "#FCE4EC"
                    button["fg"] = "#E91E63"

            def on_leave(event):
                """添加鼠标移出响应

                Args:
                    event (event): 触发事件
                """
                if button["fg"] != "#FF9800":
                    button["bg"] = "#FFFFFF"
                    button["fg"] = "#000000"

            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

        button = tk.Button(
            master,
            text=text,
            font=("微软雅黑", 12),
            bg="#FFFFFF",
            fg="#000000",
            activebackground="#FFF8E1",
            activeforeground="#FF9800",
            relief=relief,
            command=command,
        )
        hoverEffect(button)
        return button

    @staticmethod
    def set_active_button(index, button_list):
        """调整按钮列表中的激活按钮

        Args:
            index (int): 要被激活的按钮在列表中的索引
            button_list (List<Button>): 按钮列表
        """
        for i, btn in enumerate(button_list):
            if i == index:
                btn["bg"] = "#FFF8E1"
                btn["fg"] = "#FF9800"
            else:
                btn["bg"] = "#FFFFFF"
                btn["fg"] = "#000000"

    @staticmethod
    def create_normal_button(master, text, command):
        """创建普通样式的按钮

        Args:
            master (widget): 父组件
            text (String): 按钮文本
            command (function): 按钮函数

        Returns:
            Button: 创建的button
        """
        return tk.Button(
            master,
            text=text,
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
            command=command,
        )

    @staticmethod
    def create_success_button(master, text, command):
        """创建success样式(绿色)的按钮

        Args:
            master (widget): 父组件
            text (String): 按钮文本
            command (function): 按钮函数

        Returns:
            Button: 创建的button
        """
        return tk.Button(
            master,
            text=text,
            font=("微软雅黑", 14, "bold"),
            bg="#1CCD6F",
            fg="#FFFFFF",
            activebackground="#1CC4CD",
            activeforeground="#FFFFFF",
            bd=0,
            relief="flat",
            cursor="hand2",
            highlightbackground="#DAA520",
            highlightthickness=1,
            command=command,
        )

    @staticmethod
    def create_danger_button(master, text, command):
        """创建danger(红色)样式的按钮

        Args:
            master (widget): 父组件
            text (String): 按钮文本
            command (function): 按钮函数

        Returns:
            Button: 创建的button
        """
        return tk.Button(
            master,
            text=text,
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
            command=command,
        )

    @staticmethod
    def create_round_rectangle_canvas(
        master, x1_gap, y1_gap, x2_gap, y2_gap, outline_color
    ):
        """绘制圆角矩形画布

        Args:
            master (widget): 父组件
            x1_gap (int): 圆角矩形和父组件左上角的x间距
            y1_gap (int): 圆角矩形和父组件左上角的y间距
            x2_gap (int): 圆角矩形和父组件右下角的x间距
            y2_gap (int): 圆角矩形和父组件右下角的y间距
            outline_color (String): 圆角矩形的边框颜色(16进制)
        """

        def update_rectangle(
            event, widget, x1_gap, y1_gap, x2_gap, y2_gap, radius=25, **kwargs
        ):
            """更新圆角矩形

            Args:
                event (event): 触发事件
                widget (widget): 需要更新圆角矩形的组件
                x1_gap (int): 圆角矩形和父组件左上角的x间距
                y1_gap (int): 圆角矩形和父组件左上角的y间距
                x2_gap (int): 圆角矩形和父组件右下角的x间距
                y2_gap (int): 圆角矩形和父组件右下角的y间距
                radius (int, optional): 圆弧的半径. Defaults to 25.
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

        canvas = tk.Canvas(master, bg="#FFFFFF", highlightthickness=0)
        canvas.rect_id = None
        canvas.bind(
            "<Configure>",
            lambda event: update_rectangle(
                event,
                canvas,
                x1_gap,
                y1_gap,
                x2_gap,
                y2_gap,
                fill="#FFFFFF",
                outline=outline_color,
                width=1,
            ),
        )
        return canvas

    @staticmethod
    def create_combobox(master, values, selected_function=None, placeholder=""):
        """创建选择框

        Args:
            master (widget): 父组件
            values (List): 选项列表
            selected_function (function, optional): 选择后触发的事件. Defaults to None.
            placeholder (str, optional): 默认显示的文本. Defaults to "".

        Returns:
            Combobox: 创建的combobox
        """
        combobox = Combobox(
            master,
            values=values,
            justify="center",
            font=("微软雅黑", 12),
            state="readonly",
        )
        if selected_function is not None:
            combobox.bind("<<ComboboxSelected>>", selected_function)
        combobox.set(placeholder)
        return combobox

    @staticmethod
    def create_entry(master, state="normal", number_validator=False):
        """创建输入框

        Args:
            master (widget): 父组件
            state (str, optional): 输入框的状态. Defaults to "normal".
            number_validator (bool, optional): 是否启用数字验证. Defaults to False.
        """

        def validate_number_input(text):
            """验证文本是否为数字或空

            Args:
                text (String): 被校验文本

            Returns:
                boolean: 文本为数字或空时返回True
            """
            return text.isdigit() or text == ""

        entry = CustomEntry(
            master, justify="center", font=("微软雅黑", 12), relief="solid", state=state
        )
        if number_validator:
            validator_number = entry.register(validate_number_input)
            entry["validate"] = "key"
            entry["validatecommand"] = (validator_number, "%P")
        return entry

    def create_radiobutton(master, text, variable, value):
        """创建单选按钮

        Args:
            master (widget): 父组件
            text (String): 按钮文本
            variable (IntVar): 按钮绑定的变量
            value (int): 按钮被选中时对应的值

        Returns:
            Radiobutton: 创建的radiobutton
        """
        return tk.Radiobutton(
            master=master,
            text=text,
            bg="#FFFFFF",
            font=("微软雅黑", 12),
            variable=variable,
            value=value,
        )


class CustomEntry(tk.Entry):
    def __init__(self, master=None, **kwargs):
        """自定义的输入框组件，继承自tkinter.Entry

        Args:
            master (widget, optional): 父组件. Defaults to None.
        """
        super().__init__(master, **kwargs)

    def write(self, text):
        """为输入框写入指定文本，若state为disabled，则不写入。否则，清除原有内容后写入指定文本，并在写入后恢复初始state

        Args:
            text (String): 要写入的文本
        """
        state = self["state"]
        if state == "disabled":
            return
        if state == "readonly":
            self["state"] = "normal"
        self.delete(0, tk.END)
        self.insert(0, text)
        if state == "readonly":
            self["state"] = "readonly"
