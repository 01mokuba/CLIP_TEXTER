# What is Texter for?
- texter will
  1. check `is_texted` flag on DB to know whether the stored PDF document is already texted and inserted to ES or not.
  2. download PDF and save it in source folder
  3. convert from PDF to text file and save it in output folder
  4. create json file and save it in json folder
  5. insert json data into ES index
  6. clear PDF, text, and json files
  7. change `is_texted` flag on DB

# How to use it?
- configure DB, ES, and AP server settings by editing `configure.ini.templete` file
- change the name of configure file to `configure.ini`
- run `python texter.py`

# Notes
- If there are huge number of PDFs in DB, it may take long time to finish it.
- If some PDF contains other than text (e.g. graph, shape, table...), text convert may fail.

# Author
- Yusuke Hirata
