### ヤフオクから購入履歴を取得してCSVファイルに作成するクラス
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from logger import set_logger


logger = set_logger(__name__)


class yahoo:
    ## コンストラクタ
    def __init__(self):
        self._urls = []


    ## ログイン
    def __login(self,driver,username,passwd):

        try:
            driver.get('https://login.yahoo.co.jp/config/login?.src=payment&lg=jp&.intl=jp&.done=https%3A%2F%2Fpayment.yahoo.co.jp')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            driver.find_element_by_id('username').send_keys(username)    
            driver.find_element_by_id('btnNext').click()
            time.sleep(1) # ★ここで待たないとpasswdを見つけれない
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "passwd"))
            )
            driver.find_element_by_id('passwd').send_keys(passwd)
            driver.find_element_by_id('btnSubmit').click()       
        except :
            logger.error("Yahoo!かんたん決済のログインに失敗しました。手動でYahoo!かんたん決済(https://login.yahoo.co.jp/config/login?.src=payment&lg=jp&.intl=jp&.done=https%3A%2F%2Fpayment.yahoo.co.jp)にログインしてご確認ください。")
        finally:
            logger.error("Amazonのログインに成功しました。")
            
            
    ## 支払い一覧から支払い明細のURL一覧を取得する
    def __getUrlList(self,driver,yyyymm):
        driver.get(f'https://details.payment.yahoo.co.jp/PaymentDetailList?_indication={yyyymm}')
        trs = driver.find_element_by_class_name("TablePayList").find_elements_by_tag_name("tr")
        maxi = len(trs)
        
        for i in range(1,maxi):
            url = trs[i].find_element_by_class_name("elBtn.decSizS.decNrm").get_attribute("href")
            self._urls.append(url)


    ## ヤフオクから購入履歴を取得してCSVファイルに保存する
    def toCsvPurchaseHistory(self,driver,username,passwd,yyyymm):
        logger.info('ヤフオクから購入履歴を取得してCSVファイルを作成開始')
        logger.info(f'toCsvPurchaseHistory({driver},{username},{passwd},{yyyymm})')

        # ログイン
        self.__login(driver,username,passwd)

        # 支払い明細のURL一覧を取得する
        self.__getUrlList(driver,yyyymm)

        ## 支払い明細から購入履歴を取得する
        for url in self._urls:
            driver.get(url)
            
            # 取扱日
            toriatsukaibi = driver.find_elements_by_class_name('modPayList')[0].find_elements_by_tag_name('dd')[0].text
            # タイトル
            title = driver.find_element_by_class_name('itemTitle').find_element_by_tag_name('a').get_attribute("text").strip()
            # 支払金額
            shiharaikingaku = driver.find_elements_by_class_name('modPayList')[1].find_elements_by_tag_name('dd')[0].text
            # 送料
            soryo = driver.find_elements_by_class_name('modPayList')[1].find_elements_by_tag_name('dd')[1].text
            # 出品者
            shuppinsha = driver.find_elements_by_class_name('modPayList')[0].find_elements_by_tag_name('dd')[2].text

            logger.info(f'{toriatsukaibi},{title},{shiharaikingaku},{soryo},{shuppinsha}')


        logger.info('ヤフオクから購入履歴を取得してCSVファイルを作成終了')