#!/usr/bin/env python

import socket, subprocess, sys
from xml.dom.minidom import parse
from cxcommon import CX_DIR, FROM_ADDR, send_mail

# Remove spaces and slashes
def sanitize(string):
  ret = "".join(string.split())
  ret = "".join(ret.split('/'))
  return ret

# Parse metadata XML filesubject
def parse_metadata(filename):
  result = {}
  document = parse(filename)
  
  # mandatory elements
  result["category"] = document.getElementsByTagName("category")[0].childNodes[0].data
  result["subject"] = document.getElementsByTagName("subject")[0].childNodes[0].data
  result["year"] = document.getElementsByTagName("year")[0].childNodes[0].data
  result["keyname"] = document.getElementsByTagName("keyname")[0].childNodes[0].data
  result["title"] = document.getElementsByTagName("title")[0].childNodes[0].data
  result["type"] = document.getElementsByTagName("type")[0].childNodes[0].data
  result["format"] = document.getElementsByTagName("format")[0].childNodes[0].data
  result["curator"] = document.getElementsByTagName("curator")[0].childNodes[0].data
  
  stereo = document.getElementsByTagName("stereo")[0].childNodes[0].data
  if (stereo == "true" or stereo == "1"):
    result["stereo"] = "Stereo"
  else:
    result["stereo"] = "Mono"
  
  # optional elements
  if (document.getElementsByTagName("subordinatetitle")):
    result["subordinatetitle"] = document.getElementsByTagName("subordinatetitle")[0].childNodes[0].data
  else:
    result["subordinatetitle"] = result["title"] # Use title if null

  # Sanitize     
  for key in result.keys():
    result[key] = sanitize(result[key])
  
  return result

#------------------------------
# Main
#------------------------------

if (len(sys.argv) == 1):
  sys.exit("Error: specify a metadata file.")

data = parse_metadata(sys.argv[1])

content_path = "%s/%s/%s/%s/%s/%s/%s/%s/%s/%s" % (CX_DIR, data["category"], data["subject"], data["year"], data["keyname"], data["title"], data["subordinatetitle"], data["stereo"], data["type"], data["format"])

# Make folder structure
subprocess.Popen("imkdir -p " + content_path, shell=True)

# Send email alert
subject = "[CX] Ready for upload"
body = """Please upload your content with the following information.  

Host: %s
Port: 1247
User: rods
Resource: 
Collection: %s
""" % (socket.getfqdn(), content_path)
send_mail(FROM_ADDR, [data["curator"]], subject, body)

