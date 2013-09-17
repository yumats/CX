#!/usr/bin/env python

import re, subprocess, sys
from subprocess import Popen, PIPE
from cxcommon import CX_DIR, FROM_ADDR, send_mail

def remove_files(err_msg):
  ret = ""
  lines = err_msg.split("\n")
  regex = re.compile("^ERROR: chksumDataObjUtil: rcDataObjChksum error for (\S+) status = -\d+ USER_CHKSUM_MISMATCH$")
  
  for line in lines:
    m = regex.match(line)
    if (m):
      cmd = "irm -f " + m.group(1)
      ret_code = subprocess.call(cmd, shell=True)
      if (ret_code == 0):
        ret = ret + "SUCCEEDED: " + cmd + "\n"
      else:
        ret = ret + "FAILED: " + cmd + "\n"

  return ret

#------------------------------
# Main
#------------------------------

if (len(sys.argv) == 1):
  sys.exit("Error: specify email addresses.")

# Verify checksum
p = Popen("ichksum -K " + CX_DIR, shell=True, stdout=PIPE, stderr=PIPE)
out_msg, err_msg = p.communicate()

# Remove corrupted files and send email alert
if (p.returncode != 0):
  rm_log = remove_files(err_msg)
  to_list = sys.argv[1:len(sys.argv)]
  subject = "[CX] File Verification Error"
  body = "Error occurred while verifying file checksum:\n\n%s\n%s\n%s" % (out_msg, err_msg, rm_log)
  send_mail(FROM_ADDR, to_list, subject, body)
  # TODO: We should irsync here.
else:
  print "CX file check: OK"
