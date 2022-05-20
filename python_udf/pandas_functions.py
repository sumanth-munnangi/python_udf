import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd

# Constants
EMAIL_CONFIG = {
    'SEND_EMAIL_SMTP_URL': "aws_smtp_url",
    'SEND_EMAIL_SMTP_PORT': 587,
    'SEND_EMAIL_SMTP_USERNAME': "aws sns username",
    'SEND_EMAIL_SMTP_PASSWORD': "aws sns password",
    'SEND_EMAIL_SENDER': "can be any name with the default email",
    'SEND_EMAIL_TO': ["list_of emails to send the message to"],
    'SEND_EMAIL_BCC': ["list_of emails in BCC"]
}


def test_module():
    print(datetime.today())


def generate_ym(year, month):
    if month in (10, 11, 12):
        return str(year) + '-' + str(month)
    else:
        return str(year) + '-0' + str(month)


def generate_lag_month(year, month, lag):
    """
    Generates a year month based on the lag provided
    """
    if month <= lag:
        lag_ym = generate_ym(year=year - 1, month=12 - (lag - month))
    else:
        lag_ym = generate_ym(year=year, month=month - lag)

    return lag_ym


def send_an_email_from_aws(message_to_be_sent):
    """
    Sends an email with the message attached to it
    """
    message = MIMEMultipart('alternative')
    message['From'] = EMAIL_CONFIG.get('SEND_ALERT_SENDER')
    message['To'] = ", ".join(EMAIL_CONFIG.get('SEND_EMAIL_TO'))
    message['Subject'] = 'DQI Alerts'
    message['BCC'] = ", ".join(EMAIL_CONFIG.get('SEND_EMAIL_BCC'))
    to_address = EMAIL_CONFIG.get('SEND_EMAIL_TO') + EMAIL_CONFIG.get('SEND_EMAIL_BCC')

    html = message_to_be_sent

    message.attach(MIMEText(html, 'html'))

    filename = "name_of_attachments.xlsx"
    attachment = open("complete path of xlsx file ---/output.xlsx",
                      "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    message.attach(part)

    mail_server = smtplib.SMTP(
        EMAIL_CONFIG.get('SEND_EMAIL_SMTP_URL'),
        EMAIL_CONFIG.get('SEND_EMAIL_SMTP_PORT')
    )
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.ehlo()
    mail_server.login(
        user=EMAIL_CONFIG.get('SEND_EMAIL_SMTP_USERNAME'),
        password=EMAIL_CONFIG.get('SEND_EMAIL_SMTP_PASSWORD')
    )
    mail_server.sendmail(
        from_addr=EMAIL_CONFIG.get('SEND_EMAIL_SENDER'),
        to_addrs=to_address,
        msg=message.as_string()
    )
    mail_server.close()


def write_dfs_to_excel(a_tuple_of_dfs):
    counter = 0
    with pd.ExcelWriter('output.xlsx') as writer:
        for _ in a_tuple_of_dfs:
            counter += 1
            _.to_excel(writer, sheet_name=f'sheet{counter}')
