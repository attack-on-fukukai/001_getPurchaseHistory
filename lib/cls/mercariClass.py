### メルカリから購入履歴を取得してCSVファイルに作成するクラス ###
from lib.logger import set_logger
import lib.common as com


logger = set_logger(__name__)


class Mercari:
    ### コンストラクタ
    def __init__(self):
        self._urls = []


    ### 支払い一覧から支払い明細のURL一覧を取得する
    def __getUrlList(self,driver):
        driver.get('https://www.mercari.com/jp/mypage/purchased/')
        elements = driver.find_elements_by_class_name("mypage-item-link")
        
        if not elements:            
        ## 自動ログインできない場合
            return False

        for element in elements:
            url = element.get_attribute("href")
            self._urls.append(url)

        return True


    ### メルカリから購入履歴を取得してCSVファイルに保存する
    def toCsvPurchaseHistory(self,driver):
        startTime = com.getStartTime()
        logger.info('メルカリから購入履歴を取得してCSVファイルの作成開始')

        ## ログイン情報は、ユーザプロファイルに書き込む        
        ## 支払い明細のURL一覧を取得する
        ret = self.__getUrlList(driver)
        if not ret:
            return False

        ## 支払い明細から購入履歴を取得する
        datas = []
        count = 0
        for url in self._urls:
            driver.get(url)
            count += 1
            data = []
            rows = driver.find_elements_by_class_name('transact-info-table-row')
            # 購入日
            wrk = rows[2].text.splitlines()
            wrk = wrk[1].split()[0]
            data.append(wrk)
            wrk = rows[0].text.splitlines()
            # 商品タイトル
            data.append(wrk[1])
            # 購入価格
            wrk[2] = wrk[2].replace('¥','').replace(',','').strip()
            data.append(wrk[2])
            # 送料
            wrk = rows[1].text.splitlines()
            if wrk[1] == '送料込み(出品者負担)':
                wrk[1] = 0
            else:
                wrk[1] = wrk[1].replace('¥','').replace(',','').strip()
            data.append(wrk[1])
            # 出品者ID
            wrk = driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/section[2]/div/a/figure/figcaption/div').text
            wrk = wrk.strip()
            data.append(wrk)
            # 取引ID
            wrk = driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/section[1]/div/ul/li[4]/ul/li').text
            data.append(wrk)

            datas.append(data)

        ## CSVファイルを作成する
        com.toCsv(datas,com.mercariFileName)

        endTime = com.getEndTime(startTime)        
        logger.info(f'メルカリから購入履歴を取得してCSVファイルの作成終了 >> {count}件取得 処理時間：{endTime} 秒')

        return True