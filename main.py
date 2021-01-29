### mainモジュール ###
import eel
from lib.logger import set_logger
import lib.desktop as desktop
import lib.common as com
import cls.yahooClass as yahooClass
import cls.amazonClass as amazonClass
import cls.mercariClass as mercariClass


logger = set_logger(__name__)


@ eel.expose
### 設定ファイルから全ユーザー名を取得する
def getUserList():
    userList = []
    for i in range(1,6):
        user = com.getIniValue(f'User{i}','id')
        userList.append(user)
    return userList


@ eel.expose
### 購入履歴を取得してCSVファイルを作成する
def toCsvPurchaseHistory(profile,type):
    try:        
        driver = com.set_driver('chromedriver.exe',False,profile)
    except Exception:
        logger.error('ブラウザの起動に失敗しました。')


    if type == 'yahoo':
    # ヤフオク
        ec = yahooClass.yahoo()
    elif type == 'amazon':
    # Amazon
        ec = amazonClass.amazon()
    elif type == 'mercari':
    # メルカリ
        ec = mercariClass.mercari()        
    ec.toCsvPurchaseHistory(driver)
    driver.close()
    eel.view_completion_js() # 完了メッセージを表示する


### main処理
def main():
    ## 画面を表示する
    desktop.start('html','index.html',(550,400))


if __name__ == '__main__':
    main()