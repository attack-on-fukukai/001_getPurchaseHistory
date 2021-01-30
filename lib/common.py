### 独自共通関数モジュール ###
import os
import time
import datetime
import math
import configparser
from selenium.webdriver import Chrome, ChromeOptions
import pandas as pd


### 定数
# CSVファイル名
yahooFileName = 'ヤフオクの購入履歴'
amazonFileName = 'Amazonの購入履歴'
mercariFileName = 'メルカリの購入履歴'


### 設定ファイルから値を取得する
def getIniValue(section,kye):
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8_sig')
    return config[section][kye]


### Chromeを起動する関数
def set_driver(driver_path,headless_flg,profile):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg==True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')    
    options.add_argument(f'--user-data-dir={profile}') # ユーザーデータフォルダの場所

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + '\\' + driver_path,options=options)


### 開始時間を取得する
def getStartTime():
    return time.perf_counter()


### 修了時間を取得する
def getEndTime(startTime):
    return math.floor(time.perf_counter() - startTime)


### 現在日時秒を取得する
def getNow():
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    return now.strftime('%Y%m%d%H%M%S')


### CSVファイルを作成する
def toCsv(dataList,fileName):
    fileName = fileName + f'_{getNow()}.csv'
    df = pd.DataFrame(dataList,columns=['購入日', '商品タイトル', '購入価格','送料','出品者ID','取引ID'])
    df.to_csv(fileName, index=False,encoding = 'utf-8_sig')