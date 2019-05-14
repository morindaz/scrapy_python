
import pdfplumber

with pdfplumber.open('众安在线财产保险股份有限公司个人中高端医疗保险条款(2017版-B款).pdf') as pdf:
    first_page = pdf.pages[0]
    print(first_page.chars[0])

# if __name__ == '__main__':
#     with open('众安在线财产保险股份有限公司个人中高端医疗保险条款(2017版-B款).pdf', "rb") as my_pdf:
#         pdf_plumer(my_pdf)
#         # print(read_pdf(my_pdf))

