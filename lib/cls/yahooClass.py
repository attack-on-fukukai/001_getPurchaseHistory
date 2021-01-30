### ヤフオクから購入履歴を取得してCSVファイルに作成するクラス ###
import selenium.common.exceptions as exceptions
from lib.logger import set_logger
import lib.common as com


logger = set_logger(__name__)


class Yahoo:
    ### コンストラクタ
    def __init__(self):
        self._urls = []

            
    ### 支払い一覧から支払い明細のURL一覧を取得する
    def __getUrlList(self,driver):    
        driver.get('https://details.payment.yahoo.co.jp/PaymentDetailList')
        trs = driver.find_element_by_class_name("TablePayList").find_elements_by_tag_name("tr")
        maxi = len(trs)        
        for i in range(1,maxi):            
            url = trs[i].find_elements_by_tag_name('td')[3].find_element_by_class_name('elBtn.decSizS.decNrm').get_attribute('href')
            self._urls.append(url)


    ### フルネームの商品タイトルを取得する
    def __getFullTitle(self,driver,url):
        wrk = driver.find_element_by_xpath('//*[@id="itemnm"]/a').get_attribute('text').strip()
        try:
            ## 詳細ページからフル商品タイトルを取得する
            driver.get(url)
            wrk = driver.find_element_by_xpath('//*[@id="ProductTitle"]/div/h1').text
        except NoSuchElementException:
            ## 詳細ページ無くなっていたら支払い明細の商品タイトルを使う
            pass
        finally:            
            return wrk

    ### ヤフオクから購入履歴を取得してCSVファイルに保存する
    def toCsvPurchaseHistory(self,driver):
        startTime = com.getStartTime()
        logger.info('ヤフオクから購入履歴を取得してCSVファイルの作成開始')

        ## ログイン情報は、ユーザプロファイルに書き込む        
        ## 支払い明細のURL一覧を取得する
        try:
            self.__getUrlList(driver)
        except exceptions.NoSuchElementException:
        ## 自動ログインできない場合
            return False

        except IndexError:
            ## 当月の利用がない場合はリストは空のままとする
            pass
        
        ## 支払い明細から購入履歴を取得する
        datas = []
        count = 0
        for url in self._urls:
            count += 1
            driver.get(url)
            data = []
            # 購入日
            wrk = driver.find_elements_by_class_name('modPayList')[0].find_elements_by_tag_name('dd')[0].text
            wrk = wrk.split()
            data.append(wrk[0])
            # 商品タイトル
            wrk = self.__getFullTitle(driver,driver.find_element_by_xpath('//*[@id="itemnm"]/a').get_attribute("href"))
            data.append(wrk)
            # 購入価格
            driver.get(url)
            wrk = driver.find_elements_by_class_name('modPayList')[1].find_elements_by_tag_name('dd')[2].text
            wrk = driver.find_element_by_xpath('//*[@id="settlePrice"]').text
            wrk = wrk.replace(',','').replace('円','').replace('"','').strip()
            data.append(wrk)
            # 送料
            wrk = driver.find_elements_by_class_name('modPayList')[1].find_elements_by_tag_name('dd')[1].text
            wrk = wrk.replace(',','').replace('円','').replace('"','').strip()
            data.append(wrk)
            # 出品者ID            
            data.append(driver.find_element_by_xpath('//*[@id="winyid"]/a').text)
            # 取引ID
            data.append(driver.find_element_by_xpath('//*[@id="aucID"]').text)
            
            datas.append(data)

        ## CSVファイルを作成する
        com.toCsv(datas,com.yahooFileName)

        endTime = com.getEndTime(startTime)
        logger.info(f'ヤフオクから購入履歴を取得してCSVファイルの作成終了 >> {count}件取得 処理時間：{endTime} 秒')

        return True