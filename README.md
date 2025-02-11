# Windows Process Restart Utility

Small utility for checking if an executable or a python script is currently running. The intention is to regularly run this as a scheduled task.

**NOTE 1**: Currently only applicable for *.exe executables and *.py python scripts in Windows.

**NOTE 2**: For python modules, the use of ./venv as a virtual environment is required.

This utility will check the current process list for the .exe or .py of interest. If it is not found, it will attempt to start the program. After a configurable amount of retries, it will give up and optionally send an email that the program is down and could not be restarted.

## Build Instructions

1. (optional) If you wish to receive email alerts, update email_alert.py with the SMTP server and port of your provider.
1. Bundle main.py into an executable. If using pyinstaller (recommended), the following will create a one-file exe with no console.
    - (optional) Rename main.exe if it is too generic.

    ```
    pyinstaller --onefile --windowed main.py
    ```

1. Deploy the exe and config yaml file to the local machine of interest.
1. Update the config file with the python module or exe that you want to check and email recipients for alerts.
1. Create a scheduled task (windows only) to periodically run this exe.
1. Done.
