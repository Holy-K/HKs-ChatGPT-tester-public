# ----------------------------------------------------------------------------
# extract_answer_text_between_strings.py
# 概要： text内のstring_aからstring_bの間に存在する文章を抽出する関数
# 制作者：堀 和希
# 早稲田大学　基幹理工学部　表現工学科　尾形研究室
# Email: horikazuki28@akane.waseda.jp
# -----------------------------------------------------------------------------
from turtle import st
import pandas as pd
import json

def extract_text_between_strings(text, string_a, string_b="_end")->str:
    start_index = text.find(string_a) + len(string_a)
    # print(start_index)
    if string_b == "_end":
        # print("string_b is _end")
        end_index = len(text)-1
    else:
        end_index = text[start_index:].find(string_b)+start_index - len(string_b)
        if text[start_index:].find(string_b) == -1:
            end_index = len(text)
        # print(end_index)

    if start_index == -1 or end_index == -1 or end_index < start_index:
        print("\033[31m"+"extract_answer_text_between_strings Error!!"+'\033[0m',"There is no word you specified .")
        return None
    result = text[start_index:end_index + len(string_b)]
    return result
