import tkinter as tk
from queue import Empty
from threading import Thread
from time import strftime
from pygetwindow import getActiveWindowTitle
from time import sleep


class Mask:
    """the mask window for displaying logs, to make user know processing status. The mask window only accepts the logs from procedure."""

    def __init__(self, master, log_queue):
        """the basic attribute for the mask window and initilization

        Args:
            master (tkinter.Tk): window handling
            log_queue (Queue): the communication queue between mask window and procedure
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
        """create a text controller to display the log

        Returns:
            tkinter.Text: a text controller
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
        """write logs on the text controller

        Args:
            log (List): a length-2 list, the first element is the content of the log, the second element is the tag of the log ("INF1", "INF2", "ERR")
        """
        # add text controller if less than maximum num
        if len(self.text_list) < self.MAX_NUM_TEXT:
            text = self.create_text()
            text.grid(row=len(self.text_list), column=0, padx=0, pady=0)
            self.text_list.append(text)
        # delete the oldest text controller and add a new text controller, justify the row parameter to scroll logs display 
        else:
            text = self.text_list.pop(0)
            text.destroy()
            for i, text in enumerate(self.text_list):
                text.grid(row=i, column=0, padx=0, pady=0)
            text = self.create_text()
            text.grid(row=self.MAX_NUM_TEXT - 1, column=0, padx=0, pady=0)
            self.text_list.append(text)
        # write time
        text = self.text_list[-1]
        text.insert(tk.END, "[" + strftime("%H:%M:%S"), "TIME")
        # write log level
        text.insert(tk.END, " " + log[1][0:3], log[1][0:3])
        text.insert(tk.END, "] ", "TIME")
        # write log content
        text.insert(tk.END, log[0], log[1])
        self.master.update()

    def check_queue(self):
        """check is there any information in the communication queue that needs to be written
        """
        while True:
            try:
                # only show logs when the activated window is game
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
    """launch the mask window

    Args:
        log_queue (Queue): the queue used to communicate between mask thread and procedure thread
    """
    mask = tk.Tk()
    logger = Mask(mask, log_queue)
    mask.mainloop()
