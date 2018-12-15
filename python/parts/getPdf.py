import mysql.connector
import os

pdfdir = "/home/hirata_y/texter/source/"
db = mysql.connector.connect(user='clip', password='socialhackday', host='clip-rds.cshigfe65cmx.ap-northeast-1.rds.amazonaws.com', database='clipdb', charset='utf8')
cursor = db.cursor()

#cursor.execute('SELECT * FROM document WHERE is_texted = 0')
cursor.execute('SELECT * FROM document WHERE is_texted = 1')
rows = cursor.fetchall()  
for i in rows:
  docid = i[0]
  url = i[1]
  wget = "wget -O " + pdfdir + str(docid) + ".pdf " + url
  print(wget)
  os.system(wget)

cursor.close()
db.close()
