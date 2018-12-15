from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from elasticsearch import Elasticsearch
import mysql.connector
import os
import sys
import json
import collections as cl
import certifi
import datetime
import ConfigParser
 
# configuration 
config = ConfigParser.SafeConfigParser()
config.read('config.ini')
pdfdir = config.get('dirconfig', 'pdfdir')
txtdir = config.get('dirconfig', 'txtdir')
jsondir = config.get('dirconfig', 'jsondir')
es_endpoint = config.get('esconfig', 'endpoint')
es_index = config.get('esconfig', 'index')
es_type  = config.get('esconfig', 'type')
es = Elasticsearch([es_endpoint])
dbconf = {
    'user': config.get('dbconfig', 'user'),
    'password': config.get('dbconfig', 'password'),
    'host': config.get('dbconfig', 'host'),
    'database': config.get('dbconfig', 'database'),
    'charset': 'utf8'
}

# get PDF URL from DB
def get_pdf(db):
    return_val = []
    cursor = db.cursor()
    cursor.execute('SELECT * FROM document WHERE is_texted = 0')
    rows = cursor.fetchall()
    for i in rows:
        rowid = i[0]
        docid = str(rowid)
        url = i[1]
        wget = "wget -O " + pdfdir + docid + ".pdf " + url
        os.system(wget)
        return_val.append(docid)

    cursor.close()
    return return_val

# read PDF to find text
def find_textboxes_recursively(layout_obj):
    if isinstance(layout_obj, LTTextBox):
        return [layout_obj]

    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(find_textboxes_recursively(child))

        return boxes

    return []

# convert from PDF to text
def convert_to_txt(docid):
    laparams = LAParams(detect_vertical=True)
    resource_manager = PDFResourceManager()
    device = PDFPageAggregator(resource_manager, laparams=laparams)
    interpreter = PDFPageInterpreter(resource_manager, device)
    source_pdf = pdfdir + docid + ".pdf"
    output_txt = txtdir + docid + ".txt"
    output_file = open(output_txt, 'w')
    with open(source_pdf, 'rb') as f:
        for page in PDFPage.get_pages(f):
            interpreter.process_page(page)
            layout = device.get_result()
            boxes = find_textboxes_recursively(layout)
            boxes.sort(key=lambda b: (-b.y1, b.x0))

            for box in boxes:
                txt = box.get_text().strip()
                #print(txt).encode('utf-8')
                output_file.write(txt)

    output_file.close()

# get txt data
def get_text(docid):
    txtpath = txtdir + docid + '.txt'
    txtfile = open(txtpath)
    Allf = txtfile.read()  # read text data from file
    text1 = Allf.replace('\n','')
    text2 = text1.replace('\r','')
    txtfile.close()
    return text2

# put to ES
def put_to_es(db,docid):
    # fetch DB record
    cursor1 = db.cursor()
    cursor1.execute("SELECT * FROM document WHERE id = '%s'" % docid)
    docrow = cursor1.fetchone()
    pdfurl = docrow[1]
    pageid = docrow[2]
    pdate = docrow[4]
    cursor1.close()

    cursor2 = db.cursor()
    cursor2.execute("SELECT title,ministry,ministry_id,url FROM page WHERE id = '%s'" % pageid)
    pagerow = cursor2.fetchone()
    title = pagerow[0]
    print(title)
    ministry = pagerow[1]
    ministry_id = pagerow[2]
    htmlurl = pagerow[3]
    cursor2.close()
 
    # create json record
    text = get_text(docid)
    jsonpath = jsondir + docid + '.json'
    data = cl.OrderedDict()
    data["title"] = title
    data["text"] = text
    data["ministry_name"] = ministry
    data["ministry_id"] = ministry_id
    data["page_url"] = htmlurl
    data["doc_url"] = pdfurl
    data["pdate"] = pdate.strftime('%Y-%m-%d')
    jsoncontent = json.dumps(data,sort_keys=True,ensure_ascii=False,indent=4).encode('utf-8')
    with open(jsonpath,'w') as fh:
        fh.write(jsoncontent)

    # put to ES
    es.index(index=es_index, doc_type=es_type, id=docid, body=jsoncontent)

# clean up
def clean_up(db,docid):
    pdfpath = pdfdir + docid + ".pdf"
    txtpath = txtdir + docid + ".txt"
    jsonpath = jsondir + docid + ".json"

    # remove used files
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

    # change texted flag on DB
    cursor = db.cursor()
    cursor.execute("UPDATE document SET is_texted = 1 WHERE id = '%s'" % docid)
    db.commit()
    cursor.close()

    print("cleaner succeeded")

def main():
    db = mysql.connector.connect(**dbconf)
    docs = get_pdf(db)
    for docid in docs:
        print(docid)
        convert_to_txt(docid)
        put_to_es(db,docid)
        clean_up(db,docid)

    db.close()

main()
