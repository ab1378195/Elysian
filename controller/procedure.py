from threading import Thread
from controller.mask import launch_mask
from queue import Queue, Empty
from service.launch import Launch
from service.Elysian import Elysian


class Procedure:
    """the class to manage the flow of tasks performed"""

    def __init__(self):
        """basic attributes"""
        self.log_queue = Queue()
        self.mask_thread = Thread(
            target=launch_mask, args=(self.log_queue,), daemon=True
        )
        self.mask_thread.start()

    def write_log(self, log):
        """write log by sending logs to mask window

        Args:
            log (List): a length-2 list, the first element is the content of the log, the second element is the tag of the log ("INF1", "INF2", "ERR")
        """
        self.log_queue.put(log)

    def receive(self, queue):
        """keep listening to other threads, manage to send logs by other threads to mask window, terminate when accepts "exit"

        Args:
            queue (Queue): the communication queue between procedure and other threads
        """
        while True:
            try:
                log = queue.get(timeout=5)
                if log[0] == "exit":
                    break
                self.write_log(log)
            except Empty:
                pass
            except Exception as e:
                self.log_queue.put([e, "ERR"])

    def perform_tasks(self, tasks_list):
        """manage the flow of performing tasks

        Args:
            tasks_list (List<int>): tasks list, 1 means this task needs to be done, 0 means not
        """
        self.write_log(["任务开始", "INF2"])
        launch_thread_queue = Queue()
        launch = Launch(launch_thread_queue)
        launch_thread = Thread(target=launch.launch_game, daemon=True)
        launch_thread.start()
        self.receive(launch_thread_queue)
        if tasks_list[5]==1:
            Elysian_deep_thread_queue = Queue()
            elysian = Elysian(Elysian_deep_thread_queue)
            Elysian_deep_thread = Thread(target=elysian.run, daemon=True)
            Elysian_deep_thread.start()
            self.receive(Elysian_deep_thread_queue)
        self.write_log(["所有任务均已完成", "INF2"])
