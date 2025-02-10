import psutil
from psutil import AccessDenied


KEY_DIR = "process-info"
KEY_MODULE_NAME = "main.exe"


if __name__ == "__main__":
    for proc in psutil.process_iter():
        try:
            if proc.name() == KEY_MODULE_NAME and KEY_DIR in proc.cmdline()[0]:
                # print(proc)
                print("--FOUND--")
                print(proc.cmdline())
        except AccessDenied as e:
            print(e)
            # print(type(e))
            print("Access denied, skipping...")
