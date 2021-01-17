### Amazonから購入履歴を取得してCSVファイルに作成するクラス
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
    def __login(self,driver,ap_email,ap_password):

        try:
            driver.get('https://www.amazon.co.jp/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.co.jp%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=jpflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&')

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            driver.find_element_by_id('ap_email').send_keys(ap_email)
            driver.find_element_by_id('continue').click()
            time.sleep(1) # ★ここで待たないとpasswdを見つけれない
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            driver.find_element_by_id('ap_password').send_keys(ap_password)
            driver.find_element_by_id('signInSubmit').click()       
        except :
            logger.error("Amazonのログインに失敗しました。")
        finally:
            logger.error("Amazonのログインに成功しました。")
            
            
    ## 支払い一覧から支払い明細のURL一覧を取得する
    def __getUrlList(self,driver,yyyymm):
        driver.get(f'https://www.amazon.co.jp/gp/css/order-history?ref_=nav_orders_first')
        trs = driver.find_element_by_class_name("TablePayList").find_elements_by_tag_name("tr")
        maxi = len(trs)
        
        for i in range(1,maxi):
            url = trs[i].find_element_by_class_name("elBtn.decSizS.decNrm").get_attribute("href")
            self._urls.append(url)


    ## Amazonから購入履歴を取得してCSVファイルに保存する
    def toCsvPurchaseHistory(self,driver,ap_email,ap_password):
        logger.info('Amazonから購入履歴を取得してCSVファイルを作成開始')
        logger.info(f'toCsvPurchaseHistory({driver},{ap_email},{ap_password})')

        # ログイン
        self.__login(driver,ap_email,ap_password)

        logger.info('Amazonから購入履歴を取得してCSVファイルを作成終了')