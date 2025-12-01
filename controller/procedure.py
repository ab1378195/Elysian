from threading import Thread
from controller.mask import launch_mask
from queue import Queue, Empty
from service.launch import Launch
from service.material import Material
from service.home import Home


class Procedure:
    def __init__(self):
        """用于控制任务执行并与遮罩窗口通信的类"""
        self.log_queue = Queue()
        self.mask_thread = Thread(
            target=launch_mask, args=(self.log_queue,), daemon=True
        )
        self.mask_thread.start()

    def write_log(self, log):
        """发送日志给遮罩窗口显示

        Args:
            log (List): 要显示的日志
        """
        self.log_queue.put(log)

    def receive(self, queue):
        """持续监听指定线程，并传递线程的日志信息给遮罩窗口

        Args:
            queue (Queue): 和其它线程之间的通信队列
        """
        while True:
            try:
                log = queue.get(timeout=5)
                if log[0] == "exit":
                    break
                self.write_log(log)
            except Empty:
                pass
            # except Exception as e:
            #     self.log_queue.put([e, "ERR"])

    def perform_tasks(self, tasks_list):
        """执行所选的各项任务

        Args:
            tasks_list (List<int>): 任务清单列表，1代表需要执行，0代表不执行
        """
        self.write_log(["任务开始", "INF2"])
        # 启动崩坏3
        launch_thread_queue = Queue()
        launch = Launch(launch_thread_queue)
        launch_thread = Thread(target=launch.launch_game, daemon=True)
        launch_thread.start()
        self.receive(launch_thread_queue)
        # 判断并执行材料活动任务
        if tasks_list[0] == 1:
            material_thread_queue = Queue()
            material = Material(material_thread_queue)
            material_thread = Thread(target=material.run, daemon=True)
            material_thread.start()
            self.receive(material_thread_queue)
        # 判断并执行家园日常任务
        if tasks_list[1] == 1:
            home_thread_queue = Queue()
            home = Home(home_thread_queue)
            home_thread = Thread(target=home.run, daemon=True)
            home_thread.start()
            self.receive(home_thread_queue)

        # if tasks_list[5] == 1:
        #     Elysian_deep_thread_queue = Queue()
        #     elysian = Elysian(Elysian_deep_thread_queue)
        #     Elysian_deep_thread = Thread(target=elysian.run, daemon=True)
        #     Elysian_deep_thread.start()
        #     self.receive(Elysian_deep_thread_queue)
        self.write_log(["所有任务均已完成", "INF2"])
