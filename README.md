# Windows Process Status Utility

**NOTE**: Currently only applicable for *.exe executables and *.py python scripts in Windows.

This is a small utility for checking if a particular executable or a particular python script is currently running. The intention is to regularly run this as a scheduled task.

## Build Instructions

1. Update email_alert.py with the SMTP server and port of your choice for email alerts.
1. Bundle main.py into an executable. If using pyinstaller (recommended), the following will create a one-file exe with no console.
    - (optional) Rename main.exe if it is too generic.

    ```
    pyinstaller --onefile --windowed main.py
    ```

1. Deploy the exe and config yaml file to the local machine.
1. Update the config file with python module or exe that you want to check and email recipients for alerts.
1. Create a scheduled task (windows only) to periodically run this exe.
1. Done.
