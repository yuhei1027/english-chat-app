import logging
import random
import time
import os
from datetime import datetime
from zoneinfo import ZoneInfo

class MyLogger:
    def __init__(self,header,filename='./log/log.csv',output_path='./log/log.csv'):
        # CSVファイルの設定

        # ファイルが存在しない場合のみヘッダーを書き込む
        if not os.path.exists(filename):
            with open(filename, mode='w', encoding='utf-8') as f:
                f.write(header + '\n')

        # ロガーの設定
        self.logger = logging.getLogger('ProgressLogger')
        self.logger.setLevel(logging.INFO)

        # ファイルハンドラー設定（CSV形式）
        file_handler = logging.FileHandler(filename, mode='a', encoding='utf-8')

        # CSV形式のフォーマッター設定（カンマ区切り）
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)

        # ロガーにハンドラーを追加
        self.logger.addHandler(file_handler)
    
    def write_log(self,s):
        # CSV形式でログを出力
        self.logger.info(s)

def get_datetime():
    # Asia/Tokyo の現在日時を取得
    return datetime.now(tz=ZoneInfo("Asia/Tokyo")).strftime('%Y-%m-%d %H:%M:%S')
