import tkinter as tk
from queue import Empty
from threading import Thread
from time import strftime
from pygetwindow import getActiveWindowTitle
from time import sleep


class Mask:
    def __init__(self, master, log_queue):
        """遮罩窗口，用于在任务执行过程中显示日志信息

        Args:
            master (Tk): tkinter窗口句柄
            log_queue (Queue): 通信队列，从Procedure处获取要显示的日志信息
        """
        self.master = master
        self.TRANSCOLOUR = "gray"
        self.master.geometry("500x350+50+750")
        self.master.overrideredirect(True)
        self.master.wm_attributes("-transparentcolor", self.TRANSCOLOUR)
        self.master.attributes("-topmost", "true")
        self.master.configure(bg=self.TRANSCOLOUR)
        self.log_queue = log_queue
        self.text_list = []
        self.MAX_NUM_TEXT = 10
        self.communication_thread = Thread(target=self.check_queue, daemon=True)
        self.communication_thread.start()

    def create_text(self):
        """创建一个Text控件

        Returns:
            Text: 创建的Text控件
        """
        text = tk.Text(
            self.master,
            bg=self.TRANSCOLOUR,
            fg="#FFFFFF",
            font=("Arial", 12),
            bd=0,
            height=1,
        )
        text.tag_configure("TIME", foreground="#C0C0C0", font=("Arial", 12))
        text.tag_configure("INF1", foreground="#FFFFFF", font=("宋体", 12))
        text.tag_configure("INF2", foreground="#04DBDD", font=("宋体", 12))
        text.tag_configure("ERR", foreground="#FF0000", font=("宋体", 12))
        return text

    def write_log(self, log):
        """书写日志信息

        Args:
            log (List): 含两个元素的列表，第一个为日志信息，第二个为日志等级
        """
        # 当Text组件数未达上限时，继续添加Text组件
        if len(self.text_list) < self.MAX_NUM_TEXT:
            text = self.create_text()
            text.grid(row=len(self.text_list), column=0, padx=0, pady=0)
            self.text_list.append(text)
        # Text组件数到达上限后删除最老的Text组件，并调整其它Text组件的位置
        else:
            text = self.text_list.pop(0)
            text.destroy()
            for i, text in enumerate(self.text_list):
                text.grid(row=i, column=0, padx=0, pady=0)
            text = self.create_text()
            text.grid(row=self.MAX_NUM_TEXT - 1, column=0, padx=0, pady=0)
            self.text_list.append(text)
        # 书写当前时间
        text = self.text_list[-1]
        text.insert(tk.END, "[" + strftime("%H:%M:%S"), "TIME")
        # 书写日志等级
        text.insert(tk.END, " " + log[1][0:3], log[1][0:3])
        text.insert(tk.END, "] ", "TIME")
        # 书写日志内容
        text.insert(tk.END, log[0], log[1])
        self.master.update()

    def check_queue(self):
        """检查是否有日志需要被书写"""
        while True:
            try:
                # 仅在当前激活窗口为崩坏3时显示遮罩窗口
                if getActiveWindowTitle() == "崩坏3":
                    self.master.deiconify()
                else:
                    self.master.withdraw()
                log = self.log_queue.get_nowait()
                self.master.after(0, self.write_log, log)
            except Empty:
                sleep(0.5)
            except Exception as e:
                self.master.after(0, self.write_log, [e, "ERR"])


def launch_mask(log_queue):
    """启动遮罩窗口

    Args:
        log_queue (Queue): 与Procedure之间的通信队列
    """
    mask = tk.Tk()
    logger = Mask(mask, log_queue)
    mask.mainloop()
