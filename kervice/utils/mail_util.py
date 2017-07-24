# -*- coding: utf-8 -*-
import logging
import smtplib
import socket
from email.mime.text import MIMEText
import os
import gevent

log = logging.getLogger("email")


def send_mail(title=u"邮件标题", content=u"邮件内容", receviers=None):
    '''发送邮件'''

    gevent.spawn(_send_mail, title=title, content=content, receviers=receviers).start()


def _send_mail(title=u"邮件标题", content=u"邮件内容", receviers=None):
    '''发送邮件'''

    log.info(u"send mail:{}".format(title))

    # 发件人设置
    mail_host = os.getenv("MAIL_HOST")
    mail_user = os.getenv("MAIL_USER")
    mail_pass = os.getenv("MAIL_PASS")

    receviers = receviers or [mail_user]

    msg = MIMEText(content, _subtype='plain', _charset='gb2312')
    msg['Subject'] = socket.gethostbyname(socket.gethostname()) + ": " + title
    msg['From'] = mail_user
    msg['To'] = ";".join(receviers)

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(mail_user, receviers, msg.as_string())
        server.close()
        return True
    except Exception as e:
        log.error(e)
        return False


if __name__ == "__main__":
    # send_mail(
    #     title=u'邮件发不出来',
    #     content=u'邮件就是发不出来',
    #     receviers=["baiyunhui@juxinli.com"]
    # )
    _send_mail(
        title=u'邮件发不出来',
        content=u'邮件就是发不出来',
        receviers=["baiyunhui@juxinli.com"]
    )
