#!/usr/bin/env python

import re, sys
from subprocess import Popen, PIPE
from cxcommon import FROM_ADDR, send_mail

if (len(sys.argv) == 1):
  sys.exit("Error: specify email addresses.")

# List resources
p = Popen("ilsresc", shell=True, stdout=PIPE, stderr=PIPE)
stdout, stderr = p.communicate()
resources = stdout.split('\n')
pattern = re.compile("\(resource group\)")
msg = ""

# Check connection to each server
for resc in resources:
  if (resc != "" and len(pattern.findall(resc)) == 0): 
    p = Popen("ips -R " + resc, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if (p.returncode != 0):
      msg +=  "Resource: " + resc + "\n"
      msg +=  stdout
      msg +=  stderr
      msg +=  '------------------------------\n'

# Send email alert
if (msg):
  to_list = sys.argv[1:len(sys.argv)]
  subject = "[CX] Network Connection Error"
  body = "Error occurred while checking network connection:\n\n" + msg
  send_mail(FROM_ADDR, to_list, subject, body)
else:
  print "CX network check: OK"

