import sys

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTContainer, LTTextBox
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage


def find_textboxes_recursively(layout_obj):
    if isinstance(layout_obj, LTTextBox):
        return [layout_obj]

    if isinstance(layout_obj, LTContainer):
        boxes = []
        for child in layout_obj:
            boxes.extend(find_textboxes_recursively(child))

        return boxes

    return []

laparams = LAParams(detect_vertical=True)
resource_manager = PDFResourceManager()
device = PDFPageAggregator(resource_manager, laparams=laparams)
interpreter = PDFPageInterpreter(resource_manager, device)
sourcedir = "/home/hirata_y/texter/source/"
source_pdf = sourcedir + sys.argv[1] + ".pdf"
outputdir = "/home/hirata_y/texter/output/"
output_txt = outputdir + sys.argv[1] + ".txt"
output_file = open(output_txt, 'w')

def print_and_write(txt):
    print(txt).encode('utf-8')
    output_file.write(txt)
    #output_file.write('\n')

with open(source_pdf, 'rb') as f:
    for page in PDFPage.get_pages(f):
        # print_and_write('\n====== separator ======\n')
        interpreter.process_page(page)
        layout = device.get_result()
        boxes = find_textboxes_recursively(layout)
        boxes.sort(key=lambda b: (-b.y1, b.x0))

        for box in boxes:
            # print_and_write('-' * 10)
            print_and_write(box.get_text().strip())

output_file.close()
