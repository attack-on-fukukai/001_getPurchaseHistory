### mainモジュール ###
import datetime
from dateutil.relativedelta import relativedelta
import eel
from lib.logger import set_logger
import lib.desktop as desktop
import lib.common as com
import cls.yahooClass as YahooClass
import cls.amazonClass as AmazonClass
import cls.mercariClass as MercariClass


logger = set_logger(__name__)


@ eel.expose
### 設定ファイルから全ユーザー名を取得する
def getProfileList():
    wrkList = []
    for i in range(1,6):
        wrkItem = com.getIniValue('Profile',f'id{i}')
        wrkList.append(wrkItem)
    return wrkList

@ eel.expose
### ヤフオクコンボの要素を取得する
def getYahooList():
    wrkList = []
    today = datetime.date.today()
    for i in range(0,37):
        wrkItem = today - relativedelta(months=i)
        wrkItem = wrkItem.strftime('%Y年%m月')
        wrkList.append(wrkItem)
    return wrkList

@ eel.expose
### Amazonコンボの要素を取得する
def getAmazonList():
    wrkList = []
    today = datetime.date.today()
    for i in range(0,3):
        wrkItem = today - relativedelta(years=i)
        wrkItem = wrkItem.strftime('%Y年')
        wrkList.append(wrkItem)
    return wrkList

@ eel.expose
### 購入履歴を取得してCSVファイルを作成する
def toCsvPurchaseHistory(profile,type,kikan):
    driver = com.set_driver('chromedriver.exe',False,profile)
    if type == 'yahoo':
    # ヤフオク
        ec = YahooClass.Yahoo()
    elif type == 'amazon':
    # Amazon
        ec = AmazonClass.Amazon()
    elif type == 'mercari':
    # メルカリ
        ec = MercariClass.Mercari()            
    if ec.toCsvPurchaseHistory(driver,kikan):
    # 成功
        driver.quit()
        eel.view_completion_js() # 完了メッセージを表示する
    else:
    # 失敗
        logger.error('自動ログインに失敗しました。')
        eel.view_loginRequest_js() # 手動ログインを促すメッセージを表示する

### main処理
def main():
    ## 画面を表示する
    desktop.start('html','index.html',(550,400))


if __name__ == '__main__':
    main()