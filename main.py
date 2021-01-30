### mainモジュール ###
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
    profileList = []
    for i in range(1,6):
        profile = com.getIniValue('Profile',f'id{i}')
        profileList.append(profile)
    return profileList


@ eel.expose
### 購入履歴を取得してCSVファイルを作成する
def toCsvPurchaseHistory(profile,type):
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
    if ec.toCsvPurchaseHistory(driver):
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