from service.privilege import adminPermissionAcquire
from controller.application import GUI
from service.update import Update
from multiprocessing import Process
from threading import Thread
from keyboard import wait

if __name__ == "__main__":
    adminPermissionAcquire()
    update = Update()
    update_thread = Thread(target=update.check_update, daemon=True)
    update_thread.start()
    GUI_thread = Thread(target=GUI, daemon=True)
    GUI_thread.start()
    wait("esc")
