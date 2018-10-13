#!/bin/bash

echo "[INFO] starging texter..."

while getopts s:d: OPT
do
   case $OPT in
     s) SRC=$OPTARG ;; 
     d) DEST=$OPTARG ;;
   esac
done
echo "[INFO] s arg: ${SRC}"
echo "[INFO] d arg: ${DEST}"

# source PDF check
echo "[INFO] starting source PDF check..."
echo "[INFO] source PDF: ${SRC}"
SDIR="/home/hirata_y/texter/source/${SRC}"
if [ -f ${SDIR} ]; then
   echo "[INFO] source PDF found"
else
   echo "[ERROR] source PDF not found"
   exit 1
fi
echo "[INFO] finished source PDF check"

# destination file check
echo "[INFO] starting destination file check..."
echo "[INFO] destination file: ${DEST}"
DDIR="/home/hirata_y/texter/output/${DEST}"
if [ -f ${DDIR} ]; then
   echo "[INFO] destination file found"
else
   echo "[WARN] destination file does not exit"
   touch ${DDIR}
   echo "[INFO] created destination file"
fi
echo "[INFO] finished destination file check"

# converting from PDF to text
echo "[INFO] converting from PDF to text..."
python /home/hirata_y/texter/python/texter.py ${SDIR} ${DDIR}
echo "[INFO] finished converting"
exit 0
