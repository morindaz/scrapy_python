#!/usr/bin/env python
import pdfplumber
import os
import re

class Pdf2txt(object):
    def __init__(self):
        pass

    def single_convert(self, source_path, des_dir=None):
        if not source_path.endswith(".pdf"):
            return

        if des_dir is None:
            des_path = source_path.strip(".pdf")+".txt"
        else:
            filename = os.path.basename(source_path).strip(".pdf") + ".txt"
            des_path = os.path.join(des_dir, filename)
        pdf = pdfplumber.open(source_path)
        text = ''
        for page in pdf.pages:
            try:
                page_txt = page.extract_text()
                page_end_line = page_txt.split('\n')[-1]
                if re.match(r'(\d+)', page_end_line):  # 去除页面码数
                    page_txt = page_txt.split('\n')[:-1]
                text += ''.join(page_txt)
            except:pass
        pdf.close()
        with open(des_path, "w") as fout:
            fout.write(text)
        print (source_path, ": Done!")

    def batch_convert(self, source_dir, des_dir=None):
        if des_dir is None:
            des_dir = source_dir
        for filename in os.listdir(source_dir):
            source_path = os.path.join(source_dir, filename)
            self.single_convert(source_path, des_dir)
        print ("ALL DONE! ")

if __name__ == '__main__':
    # from conf import tmp_dir
    des_dir = os.path.join("./data", "security_readme/pdf2txt_res")
    source_dir= "./data/6个条款"
    pp = Pdf2txt()
    pp.batch_convert(source_dir, des_dir)