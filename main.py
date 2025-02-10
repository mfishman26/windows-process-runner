import sys
import os
import subprocess
from time import sleep
from pathlib import Path
import psutil
from psutil import AccessDenied
import yaml
import email_alert


with open("./config.yaml", "r", encoding="UTF8") as f:
    config = yaml.safe_load(f)


MODULE_PATH = config["module_path"]
RETRY_COUNT = config["retry_count"]
RETRY_SLEEP = config["retry_sleep"]
SEND_EMAIL_ALERT = config["send_alert_emails"]
ALERT_RECIPIENTS = config["alert_recipients"]


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
            elif module_name.endswith(".exe"):
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
    if not module_name.endswith(".py") and not module_name.endswith(".exe"):
        return 3
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
        run_module(root=root_direc, module=module_name)
        print(f"Retry attempt {i + 1}")
        sleep(RETRY_SLEEP)
    return 2


if __name__ == "__main__":
    py_version = sys.version_info
    if py_version[0] < 3:
        raise Exception(f"Must use Python 3, version detected=={sys.version}")
    module_base = os.path.basename(MODULE_PATH)
    module_path = Path(MODULE_PATH)
    # module_path_abs = module_path.resolve()
    module_parent = module_path.resolve().parent
    # module_parent_base = os.path.basename(module_parent)
    res = main(root_direc=module_parent, module_name=module_base)
    if py_version[1] >= 10:
        match res:
            case 0:
                print("Process running")
            case 1:
                print("Process successfully restarted")
            case 2:
                print("Process is NOT running and was unable to be restarted")
                if SEND_EMAIL_ALERT:
                    print("Sending alert email")
                    email_alert.send_alert(
                        module_name=module_base, to_addrs=ALERT_RECIPIENTS
                    )
            case _:
                print("Unsupported module or executable, quitting...")
    else:
        # NOTE: Only for python version < 3.10
        if res == 0:
            print("Process running")
        elif res == 1:
            print("Process successfully restarted")
        elif res == 2:
            print("Process is NOT running and was unable to be restarted")
            if SEND_EMAIL_ALERT:
                email_alert.send_alert(
                    module_name=module_base, to_addrs=ALERT_RECIPIENTS
                )
        else:
            print("Unsupported module or executable, quitting...")
