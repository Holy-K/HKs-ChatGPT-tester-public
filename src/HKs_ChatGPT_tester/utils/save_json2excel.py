# ----------------------------------------------------------------------------
# save_json2excel.py
# 概要：json配列を指定のエクセルブックにページとして保存する関数
# 制作者：堀 和希
# 早稲田大学　基幹理工学部　表現工学科　尾形研究室
# Email: horikazuki28@akane.waseda.jp
# -----------------------------------------------------------------------------
import pandas as pd
import openpyxl
import datetime
def save_json2excel(experiment_log,PATH_LOG_EXCELFILE,Date=datetime.datetime.now(),sheet_name=None):
    user_sheet_name = sheet_name
    experiment_log_df = pd.DataFrame(experiment_log)
    order = 1
    while True:
        try:
            if user_sheet_name != None and order == 1:
                with pd.ExcelWriter(PATH_LOG_EXCELFILE, engine='openpyxl', mode='a') as writer:
                    experiment_log_df.to_excel(
                        writer, sheet_name=user_sheet_name)
                print("Log is saved successfully to \""+PATH_LOG_EXCELFILE+"\"")
                break
            elif user_sheet_name != None and order > 1:
                with pd.ExcelWriter(PATH_LOG_EXCELFILE, engine='openpyxl', mode='a') as writer:
                    experiment_log_df.to_excel(
                        writer, sheet_name=user_sheet_name + "(" + str(order-1) + ")" )
                print("Log is saved successfully to \""+PATH_LOG_EXCELFILE+"\"")
                break

            else:
                with pd.ExcelWriter(PATH_LOG_EXCELFILE, engine='openpyxl', mode='a') as writer:
                    experiment_log_df.to_excel(
                        writer, sheet_name=Date.strftime("%Y%m%d%H%M%S") + "-" + str(order))# 日時+order
                print("Log is saved successfully to \""+PATH_LOG_EXCELFILE+"\"")
                break
        except PermissionError as e:
            print(
                "\033[31m"+"Error!!"+'\033[0m', " Close Excel file to save log. Do you wan to try again?(y/n)")
            while True:
                _yn = input()
                if _yn == "y":
                    break
                elif _yn == "n":
                    print("Log is destroyed")
                    break
                else:
                    continue
            if _yn == "y":
                continue
            break
        except ValueError as e:
            order += 1
            continue

def ask_save_json2excel(experiment_log,PATH_LOG_EXCELFILE,Date=datetime.datetime.now(),sheet_name=None):
    if sheet_name == None:
        user_sheet_name = sheet_name
    print("Save log? (y/n)")
    while True:
        _yn = input()
        if _yn == "y":
            experiment_log_df = pd.DataFrame(experiment_log)
            order = 1
            while True:
                try:
                    if user_sheet_name != None and order == 1:
                        with pd.ExcelWriter(PATH_LOG_EXCELFILE, engine='openpyxl', mode='a') as writer:
                            experiment_log_df.to_excel(
                                writer, sheet_name=user_sheet_name)
                        print("Log is saved successfully to \""+PATH_LOG_EXCELFILE+"\"")
                        break
                    elif user_sheet_name != None and order > 1:
                        with pd.ExcelWriter(PATH_LOG_EXCELFILE, engine='openpyxl', mode='a') as writer:
                            experiment_log_df.to_excel(
                                writer, sheet_name=user_sheet_name + "(" + str(order-1) + ")" )
                        print("Log is saved successfully to \""+PATH_LOG_EXCELFILE+"\"")
                        break

                    else:
                        with pd.ExcelWriter(PATH_LOG_EXCELFILE, engine='openpyxl', mode='a') as writer:
                            experiment_log_df.to_excel(
                                writer, sheet_name=Date.strftime("%Y%m%d%H%M%S") + "-" + str(order))# 日時+order
                        print("Log is saved successfully to \""+PATH_LOG_EXCELFILE+"\"")
                        break
                except PermissionError as e:
                    print(
                        "\033[31m"+"Error!!"+'\033[0m', " Close Excel file to save log. Do you wan to try again?(y/n)")
                    while True:
                        _yn = input()
                        if _yn == "y":
                            break
                        elif _yn == "n":
                            print("Log is destroyed")
                            break
                        else:
                            continue
                    if _yn == "y":
                        continue
                    break
                except ValueError as e:
                    order += 1
                    continue
            break
        elif _yn == "n":
            print("Canceled saving log")
            break
        else:
            print("\033[31m"+"Error!!"+'\033[0m',"Input correct key(y/n)")
