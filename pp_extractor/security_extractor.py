# -*- coding:UTF-8 -*-

import pandas as pd
import os
from pp_extractor.pattern_extractor import PatternExtractor

import time
datesuffix = time.strftime("%Y-%m-%d", time.localtime())

# 加载模式字典



# 处理流程
def security_extractor():
    result_filename = "条款拆解结果" + datesuffix + ".xlsx"
    result_file = os.path.join("data/save", result_filename)
    source_dir = os.path.join("data/origin", "security_readme/")

    pattern_path = os.path.join("data", "pattern/security_item_dic.txt")
    pp = PatternExtractor()
    pp.add_pattern(pattern_path)

    writer = pd.ExcelWriter(result_file)
    for filename in os.listdir(source_dir):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(source_dir, filename)
        with open(filepath) as fin:
            text = ""
            tmp = []
            for line in fin.readlines():
                line = line.strip()
                text += line
                if line.endswith("。") or line.endswith("；"):
                    res = pp.extract(text)
                    for it in res:
                        tmp.append([filename.strip(".txt"),text, it])
                    text = ""

            # 处理责任免除/保险责任的分类，添加保险条款的字段
            results = []
            for item in tmp:
                if "；" in item[1]:
                    results.append([item[0], "保险条款", "责任免除", item[1], item[2]])
                else:
                    results.append([item[0], "保险条款", "保险责任", item[1], item[2]])

            df = pd.DataFrame(results)
            df.columns = ['条款名称', '拆分类型', '责任/责免', '话术', '标签']
            df.to_excel(writer, index=False, sheet_name=filename[-10:])
    writer.save()

# 健康告知提取
def health_note_extractor(filename):
    import re
    pattern_path = os.path.join("data", "pattern/security_item_dic.txt")
    pp = PatternExtractor()
    pp.add_pattern(pattern_path)
    filepath = os.path.join("data/origin", filename)
    result_filename = "健康告知提取结果" + datesuffix + ".xlsx"
    result_file = os.path.join("data/save", result_filename)
    writer = pd.ExcelWriter(result_file)
    fp = pd.read_excel(filepath)
    selected = list(zip(list(fp["险种责任"]), list(fp["健康告知"])))
    results = {}
    cur_ = ""
    for item in selected:
        if item[0] != cur_ and cur_:
            df = pd.DataFrame(results[cur_])
            df.columns = ["险种责任", "健康告知", "标签"]
            df.to_excel(writer, index=False, sheet_name=cur_[-5:])

        cur_ = item[0]
        try:
            if not item[0] in results:
                results[item[0]] = []
            if pd.isnull(item[1]):
                continue
            pure_text = item[1].replace(" ", "").replace("\n", "").replace("\t", "").replace("\s", "")
            res = pp.extract(pure_text)
            for it in res:
                results[item[0]].append([item[0], item[1], it])
        except:pass
    # 保存最后一个
    df = pd.DataFrame(results[cur_])
    df.columns = ["险种责任", "健康告知", "标签"]
    df.to_excel(writer, index=False, sheet_name=cur_[-5:])
    writer.save()


if __name__ == '__main__':
    filename = "健康告知20190219.xlsx"
    # health_note_extractor(filename)

    security_extractor()

