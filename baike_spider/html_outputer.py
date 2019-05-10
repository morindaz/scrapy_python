class HtmlOupter(object):
    def __init__(self):
        self.datas = list()

    def collect_data(self, new_data):
        if new_data is None:
            return
        self.datas.append(new_data)


    def output_html(self):
        fout = open("output.html", "w")
        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")
        # ascii
        for data in self.datas:
            try:
                fout.write("<tr>")
                fout.write("<td>%s</td>" % data['url'])
                fout.write("<td>%s</td>" % data['title'])
                fout.write("<td>%s</td>" % data['summary'])
                fout.write("</tr>")

            except:
                print("error writing %s" %data['title'])

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()