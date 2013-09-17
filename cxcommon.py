#!/usr/bin/env python

from smtplib import SMTP
from email.MIMEText import MIMEText

CX_DIR = '/CineGridExchange/home/rods/CineGridExchange'
FROM_ADDR = ''

def send_mail(from_addr, to_list, subject, body):
  msg = MIMEText(body)
  msg['Subject'] = subject
  msg['From'] = from_addr
  msg['To'] = ", ".join(to_list)
  s = SMTP('localhost')
  s.sendmail(from_addr, to_list, msg.as_string())
  s.quit()
