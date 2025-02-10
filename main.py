import os
import subprocess
from time import sleep
from pathlib import Path
import psutil
from psutil import AccessDenied
import email_alert


# KEY_DIR = "process-info"
# KEY_MODULE_NAME = "main.py"
# IS_PYTHON = True
MODULE_PATH = "./main.py"
RETRY_COUNT = 5
RETRY_SLEEP = 60
SEND_EMAIL_ALERT = True
ALERT_RECIPIENTS = [""]


def run_module(root: str, module: str):
    module_absolute_path = os.path.join(root, module)
    python_venv_path = os.path.join(root, "venv", "Scripts", "python.exe")
    if module.endswith(".py"):
        subprocess.run([python_venv_path, module_absolute_path], check=False)
    elif module.endswith(".exe"):
        subprocess.run([module_absolute_path], check=False)
    else:
        print(f"{module} is not a supported module type")


def search_for_process(root_direc: str, module_name: str):
    process_running = False
    for proc in psutil.process_iter():
        try:
            if module_name.endswith(".py"):
                if "python" in proc.name():
                    print(proc)
                    cmd_res = proc.cmdline()
                    if root_direc in cmd_res[0] and module_name in cmd_res[1]:
                        print("--FOUND--")
                        print(cmd_res)
                        process_running = True
                        return process_running
            else:
                if proc.name() == module_name and root_direc in proc.cmdline()[0]:
                    # print(proc)
                    print("--FOUND--")
                    print(proc.cmdline())
                    process_running = True
                    return process_running
        except AccessDenied as e:
            print(e)
            print("Access denied, skipping...")
    return process_running


def main(root_direc: str, module_name: str):
    root_base = os.path.basename(root_direc)
    search_res = search_for_process(root_direc=root_base, module_name=module_name)
    if search_res:
        return 0
    for i in range(RETRY_COUNT):
        if i > 0:
            search_res = search_for_process(
                root_direc=root_base, module_name=module_name
            )
        if search_res:
            print("Process restarted")
            return 1
        # TODO: attempt to start process
        run_module(root=root_direc, module=module_name)
        print(f"Retry attempt {i + 1}")
        sleep(RETRY_SLEEP)
    return 2


if __name__ == "__main__":
    module_base = os.path.basename(MODULE_PATH)
    module_path = Path(MODULE_PATH)
    module_parent = module_path.resolve().parent
    # module_parent_base = os.path.basename(module_parent)
    res = main(root_direc=module_parent, module_name=module_base)
    if res == 0:
        print("Process running")
    if res == 1:
        print("Process successfully restarted")
    if res == 2:
        print("Process is NOT running and was unable to be restarted")
        if SEND_EMAIL_ALERT:
            email_alert.send_alert(module_name=module_base, to_addrs=ALERT_RECIPIENTS)
