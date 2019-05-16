#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flashtext
from itertools import chain


class PatternExtractor(object):
    """
    功能：
    extract --> 抽取一串文本中 非标准名 映射的 标准名
    replace --> 将一串文本中的 非标准名 替换成 标准名
    """

    def __init__(self):
        self.ac = flashtext.KeywordProcessor()
        # 字典格式 --> "非标准名":["标准名1", "标准名2", ...]
        self.project = {}

    def add_pattern(self, filepath):
        """
        :param filepath: 必须是同一个的格式的txt文件，以\t分隔的两列，第一列是标准名，第二列是非标准名,不要header.
        :return: None
        """
        with open(filepath, "r", encoding="utf-8") as fin:
            for line in fin.readlines():
                try:
                    line = line.strip().split("\t")
                    # 如果只有一列，自动扩展非标准名
                    if len(line) == 1:
                        line.extend(line)
                    line[1] = " ".join(list(line[1]))
                    # 如果一个非标准名对应多个标准名，扩展标准名列表
                    if line[1] in self.project and not line[0] in self.project[line[1]]:
                        self.project[line[1]].append(line[0])
                    if not line[1] in self.project:
                        self.project[line[1]] = [line[0]]
                except:
                    pass

        for k, v in self.project.items():
            self.ac.add_keyword(k, "#*#".join(v))

    def extract(self, text):
        """
        抽取一串文本中 非标准名 映射的 标准名
        :param text: 文本
        :return: list: 提取到的标准词的列表
        """
        text = " ".join(list(text))
        res = self.ac.extract_keywords(text)
        results = [it.split("#*#") for it in res]
        results = list(set(chain.from_iterable(results)))
        return results

    def replace(self, text):
        """
        将一串文本中的 非标准名 替换成 标准名
        :param text: 文本
        :return: 替换后的字符串
        """
        text = " ".join(list(text))
        res = self.ac.replace_keywords(text)
        result = "".join(res.split(" "))
        return result


if __name__ == '__main__':
    import os

    pattern_path = os.path.join("./data", "pattern/security_item_dic.txt")
    pp = PatternExtractor()
    pp.add_pattern(pattern_path)
    extract_res = pp.extract('美容和整容手术和怀孕')
    print(extract_res)
    replace_res = pp.replace("美容和整容手术和怀孕")
    print(replace_res)
