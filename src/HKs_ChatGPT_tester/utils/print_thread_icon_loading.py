# ----------------------------------------------------------------------------
# print_thread_icon_loading.py
# 概要：Thread でローディングアイコンを表示するコード
# 参考:https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running
# -----------------------------------------------------------------------------
from itertools import cycle  # イテレータの組み合わせ (反復) を扱うためのライブラリ
from shutil import get_terminal_size  # ターミナルのサイズを取得するライブラリ
from threading import Thread  # スレッドを作成するライブラリ
from time import sleep  # 指定された秒数待機するライブラリ


class PrintThreadIconLoading:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1):
        """
        ローダーのようなコンテキストマネージャー

        Args:
            desc (str, optional): ローダーの説明文. デフォルトは "Loading...".
            end (str, optional): 最後の出力. デフォルトは "Done!".
            timeout (float, optional): 出力間のスリープ時間. デフォルトは 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)  # バックグラウンドで動作するスレッドを作成
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]  # アニメーションに使用する文字列の一覧
        self.done = False  # アニメーション停止フラグ

    def start(self):
        self._thread.start()  # アニメーションスレッドを開始
        return self

    def _animate(self):
        for c in cycle(self.steps):  # stepsの文字列を繰り返し使用してアニメーションを行う
            if self.done:  # アニメーション停止フラグが立ったら終了
                break
            print(f"\r{self.desc} {c}", flush=True, end="")  # 文字列を出力してカーソル位置を維持
            sleep(self.timeout)  # 指定された秒数待機

    def __enter__(self):
        self.start()  # コンテキストマネージャの開始時にアニメーションを開始

    def stop(self):
        self.done = True  # アニメーション停止フラグを立てる
        cols = get_terminal_size((80, 20)).columns  # ターミナルの幅を取得
        print("\r" + " " * cols, end="", flush=True)  # 空白文字で出力行をクリア

        print(f"\r{self.end}", flush=True)  # 終了メッセージを出力

    def __exit__(self, exc_type, exc_value, tb):
        # エラー処理はこれらの変数を使用して行います ^
        self.stop()  # コンテキストマネージャの終了時にアニメーションを停止
