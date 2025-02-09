import psutil
from psutil import AccessDenied


KEY_DIR = "process-info"
KEY_MODULE_NAME = "main.py"
IS_PYTHON = True


def main(root_direc: str, module_name: str):
    for proc in psutil.process_iter():
        try:
            if IS_PYTHON:
                if "python" in proc.name():
                    print(proc)
                    cmd_res = proc.cmdline()
                    if root_direc in cmd_res[0] and module_name in cmd_res[1]:
                        print("--FOUND--")
                        print(cmd_res)
            else:
                if proc.name() == module_name and root_direc in proc.cmdline()[0]:
                    # print(proc)
                    print("--FOUND--")
                    print(proc.cmdline())
        except AccessDenied as e:
            print(e)
            print("Access denied, skipping...")


if __name__ == "__main__":
    main(root_direc=KEY_DIR, module_name=KEY_MODULE_NAME)
