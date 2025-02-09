import psutil
from psutil import AccessDenied


KEY_DIR = "process-info"
KEY_MODULE_NAME = "main.py"


if __name__ == "__main__":
    for proc in psutil.process_iter():
        try:
            # cmd_res = proc.cmdline()
            if "python" in proc.name():
                print(proc)
                cmd_res = proc.cmdline()
                # print(cmd_res)
                if KEY_DIR in cmd_res[0] and KEY_MODULE_NAME in cmd_res[1]:
                    print("--FOUND--")
                    print(cmd_res)
        except AccessDenied as e:
            print(e)
            # print(type(e))
            print("Access denied, skipping...")
