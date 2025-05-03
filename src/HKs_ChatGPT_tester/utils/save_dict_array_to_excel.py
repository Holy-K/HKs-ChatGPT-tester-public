# ----------------------------------------------------------------------------
# save_dict_array_to_excel.py
# 概要：辞書を要素に持つ配列をJSON形式の表に直し、Excelに保存する関数
# 制作者：堀 和希
# 早稲田大学　基幹理工学部　表現工学科　尾形研究室
# Email: horikazuki28@akane.waseda.jp
# -----------------------------------------------------------------------------
import pandas as pd
import openpyxl
import datetime
def split_long_texts(df, char_limit, line_limit):
    """
    DataFrame内の文字列が指定された文字数制限または行数制限を超える場合、新しいキーを作成し、超過分の文字を新しいキーの値として設定する関数

    Args:
        df: pandas DataFrame
        char_limit: 文字数制限
        line_limit: 行数制限

    Returns:
        処理後のDataFrame
    """
    new_columns = {}

    for col in df.columns:
        number_additionalcell = 1
        while True:
            # 文字数制限または行数制限を超える値があるか確認
            if df[col].apply(lambda x: isinstance(x, str) and (len(x) > char_limit or x.count('\n') > line_limit)).any():
                new_col_name = f"{col}-{1 + number_additionalcell}"
                new_columns[new_col_name] = df[col].apply(lambda x: x[char_limit:] if isinstance(x, str) and len(x) > char_limit else ('\n'.join(x.split('\n')[line_limit:]) if isinstance(x, str) and x.count('\n') > line_limit else ''))
                df[col] = df[col].apply(lambda x: x[:char_limit] if isinstance(x, str) and len(x) > char_limit else ('\n'.join(x.split('\n')[:line_limit]) if isinstance(x, str) and x.count('\n') > line_limit else x))
                number_additionalcell += 1
            else:
                break

    # 新しい列を一度に追加
    df = pd.concat([df, pd.DataFrame(new_columns)], axis=1)
    return df


def save_dict_array_to_excel(dict_array, excel_path, save_date=datetime.datetime.now()):
    """
    辞書を要素に持つ配列をJSON形式の表に直し、Excelに保存する関数

    Args:
        dict_array: 辞書を要素に持つ配列
        excel_path: 保存するExcelのパス
        save_date: 保存日時

    Returns:
        なし
    """
    EXCEL_CEL_CHAR_LIMIT = 32767
    EXCEL_CEL_LINE_LIMIT = 253

    # 辞書配列をDataFrameに変換
    df = pd.DataFrame(dict_array)
    # DataFrame内の制限に引っかかる長文を別の列に分割
    df = split_long_texts(df, EXCEL_CEL_CHAR_LIMIT, EXCEL_CEL_LINE_LIMIT)
    # Excelファイルに新しいシートを追加して保存
    vol = 0
    while True:
        try:
            if vol >=1:
                with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a') as writer:
                    df.to_excel(writer, sheet_name=save_date.strftime("%Y%m%d%H%M%S" + "-" + str(vol)), index=False)
            else:
                with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a') as writer:
                    df.to_excel(writer, sheet_name=save_date.strftime("%Y%m%d%H%M%S"), index=False)
            print("Log is saved successfully to\""+excel_path+"\"")
            break
        except ValueError:
            vol = vol+1
        except PermissionError:
            print("\033[31m"+"Error!!"+'\033[0m', "Close Excel file to save log. Do you want to try again?(y/n)")
            while True:
                retry = input()
                if retry.lower() == "y":
                    break
                elif retry.lower() == "n":
                    print("Canceled saving log")
                    return
                else:
                    print("Please input correct key(y/n)")
                    continue
        continue
