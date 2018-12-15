from elasticsearch import Elasticsearch
import mysql.connector
import sys
import os
import json
import collections as cl
import certifi

# get text
docid = sys.argv[1]
txtdir = '/home/hirata_y/texter/output/'
txtpath = txtdir + docid + '.txt'
txtfile = open(txtpath)
text = txtfile.read()  # read text data from file
txtfile.close()

# get records from DB
db = mysql.connector.connect(user='clip', password='socialhackday', host='clip-rds.cshigfe65cmx.ap-northeast-1.rds.amazonaws.com', database='clipdb', charset='utf8')
cursor1 = db.cursor()
docid = sys.argv[1]
print(docid)

cursor1.execute("SELECT * FROM document WHERE id = '%s'" % docid)
docrow = cursor1.fetchone()
pdfurl = docrow[1]
pageid = docrow[2]
pdate = docrow[4]
cursor1.close()

cursor2 = db.cursor()
cursor2.execute("SELECT * FROM page WHERE id = '%s'" % pageid)
pagerow = cursor2.fetchone()
title = pagerow[1]
print(title)
ministry = pagerow[2]
htmlurl = pagerow[3]
cursor2.close()
db.close()

# create json record
jsondir = '/home/hirata_y/texter/json/'
jsonpath = jsondir + docid + '.json'

data = cl.OrderedDict()
data["title"] = title
data["text"] = text
data["ministry"] = ministry
data["htmlurl"] = htmlurl
data["pdfurl"] = pdfurl
data["pdate"] = pdate
jsoncontent = json.dumps(data,sort_keys=True,ensure_ascii=False,indent=4).encode('utf-8')
with open(jsonpath,'w') as fh:
   fh.write(jsoncontent)

# put into ES
es_endpoint = 'https://search-clip-uu6oh7i2l7fon6tlma23e6ax3a.ap-northeast-1.es.amazonaws.com'
es_index = 'clip'
es_type  = 'documents'
es = Elasticsearch([es_endpoint],use_ssl=True,ca_certs=certifi.where())
es.index(index=es_index, doc_type=es_type, id=docid, body=jsoncontent)
