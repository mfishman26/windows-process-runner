import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_SERVER = ""
SMTP_PORT = 0
TO_ADDR = [""]


def send_alert(module_name: str, to_addrs: list):
    server = smtplib.SMTP()
    server.set_debuglevel(1)
    server.connect(host=SMTP_SERVER, port=SMTP_PORT)
    server.ehlo()
    msg = MIMEMultipart("mixed")
    msg_alt = MIMEMultipart("alternative")
    msg["From"] = "noreply@noreply.com"
    msg["To"] = ",".join(to_addrs)
    msg["Subject"] = f"ALERT: {module_name} Down"
    html = f"""
        <html>
        <head></head>
        <body>
            <p>{module_name} is down and was unable to be restarted.</p>
        </body>
        </html>
        """
    html_attach = MIMEText(html, "html")
    msg_alt.attach(html_attach)
    msg.attach(msg_alt)
    server.sendmail(msg["From"], to_addrs, msg.as_string())
    server.quit()
    del msg
    print("Email sent")


if __name__ == "__main__":
    send_alert(TO_ADDR, "test_module.exe")
