#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:     ivan.wang
@contact:    357492882@qq.com
@others:     DTStudio, All rights reserved-- Created on 2017/10/25
@desc:       使用unittest组织用例
"""
import time
import smtplib
from email.mime.text import MIMEText

def send_mail(file_new):
    # 发件人邮箱
    mail_from = 'xinyuanjing123@126.com'
    # 收件人邮箱
    mail_to = '454353420@qq.com'
    # 定义正文
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()
    msg = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    msg['From'] = mail_from
    msg['To'] = mail_to
    # 定义标题
    msg['Subject'] = u"xxxxx项目自动化测试报告"
    # 定义发送时间（不定义的可能有的邮件客户端会不显示发送时间）
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    smtp = smtplib.SMTP()
    # 连接 SMTP 服务器，此处用的 126 的 SMTP 服务器
    smtp.connect('smtp.126.com')
    # 发件人的用户名密码
    smtp.login('xinyuanjing123@126.com', 'suiyuan123')
    smtp.sendmail(mail_from, mail_to, msg.as_string())
    smtp.quit()
    print ('email has send out !')