# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from email.mime.base import MIMEBase
from email import encoders
import os
import time


class Email_SMTP():
    def __init__(self, Host, Port, User, Pwd):
        self.SMTP_ssl_host = Host
        self.SMTP_ssl_port = Port
        self.SMTP_User = User
        self.SMTP_Pwd = Pwd

    def Send(self, send_subject, send_from, send_to, send_cc, send_bcc,
             send_atta, send_body):
        msg = MIMEMultipart()
        msg['Subject'] = send_subject
        msg['From'] = send_from
        msg['To'] = ','.join(send_to)
        msg['Cc'] = ','.join(send_cc)

        email_to = ','.join(send_to + send_cc + send_bcc)
        email_to = email_to.split(',')

        # 內文
        if send_body:
            txt = MIMEText(send_body, 'html', 'utf-8')
            msg.attach(txt)

        # 附檔
        if send_atta:
            for att in send_atta:
                ctype, encoding = mimetypes.guess_type(att)

                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'

                maintype, subtype = ctype.split('/', 1)

                with open(att, 'rb') as fp:
                    attachment = MIMEBase(maintype, subtype)
                    attachment.set_payload(fp.read())
                encoders.encode_base64(attachment)
                attachment.add_header("Content-Disposition",
                                      'attachment', filename=os.path.basename(att))
                msg.attach(attachment)

                fp.close()

        # 寄送
        times = 1
        while True:
            try:
                server = smtplib.SMTP_SSL(
                    self.SMTP_ssl_host, self.SMTP_ssl_port)
                server.login(self.SMTP_User, self.SMTP_Pwd)
                server.sendmail(send_from, email_to, msg.as_string())
                server.quit()
                print('Email is sent!!!')
                break

            except (smtplib.SMTPSenderRefused, smtplib.SMTPServerDisconnected) as n:
                print('{}. Retry [ {} ].'.format(n, times), '\r', end='')
                times += 1
                time.sleep(60)
                pass

            except (smtplib.SMTPDataError) as n:
                print(n)
                raise

            except:
                print('Unknown error.')
                raise
