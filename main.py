### mainモジュール
from logger import set_logger
import common as com
import yahooClass
import amazonClass

logger = set_logger(__name__)


## main処理
def main():
    # driverを起動
    driver = com.set_driver('chromedriver.exe',False)

    # ヤフオクから購入履歴を取得してCSVファイルを作成する
    yahoo = yahooClass.yahoo()    
    yahoo.toCsvPurchaseHistory(driver,"ヤフーID","パスワード",'取得する年月(YYYYMM)')
    
    # Amazonから購入履歴を取得してCSVファイルを作成する
    amazon = amazonClass.yahoo()
    amazon.toCsvPurchaseHistory(driver,"メールアドレス","パスワード")

    # メルカリから購入履歴を取得してCSVファイルを作成する


if __name__ == '__main__':
    main()