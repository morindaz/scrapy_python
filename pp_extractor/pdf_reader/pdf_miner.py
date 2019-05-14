from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf

def read_pdf(pdf):
    # resource manager
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    # device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    # 获取所有行
    # tmp_cnt = content.replace("\n\n", "aaaa").replace("\n", "").strip(' ')
    lines = str(content).strip().split("\n")

    return lines

if __name__ == '__main__':
    with open('众安在线财产保险股份有限公司个人中高端医疗保险条款(2017版-B款).pdf', "rb") as my_pdf:
        # pdf_plumer(my_pdf)
        print(read_pdf(my_pdf))