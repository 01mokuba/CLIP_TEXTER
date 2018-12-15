import os
import sys

pdfdir = "/home/hirata_y/texter/source/"
txtdir = "/home/hirata_y/texter/output/"
jsondir = "/home/hirata_y/texter/json/"
filename = sys.argv[1]
pdfpath = pdfdir + filename + ".pdf"
txtpath = txtdir + filename + ".txt"
jsonpath = jsondir + filename + ".json"


if os.path.isfile(pdfpath):
  os.remove(pdfpath)
  print("pdf file removed")
else:
  print("pdf file not found")

if os.path.isfile(txtpath):
  os.remove(txtpath)
  print("txt file removed")
else:
  print("txt file not found")

if os.path.isfile(jsonpath):
  os.remove(jsonpath)
  print("json file removed")
else:
  print("json file not found")

print("cleaner succeeded")
