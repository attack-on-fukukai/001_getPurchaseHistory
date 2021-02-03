### Amazonから購入履歴を取得してCSVファイルに作成するクラス ###
from lib.logger import set_logger
import lib.common as com


logger = set_logger(__name__)


class Amazon:
    ### コンストラクタ
    def __init__(self):
        self._urls = []

            
    ### 支払い一覧から支払い明細のURL一覧を取得する
    def __getUrlList(self,driver,kikan):

        if kikan == '過去30日間':
            kikan = 'last30'
        elif kikan == '過去3か月':
            kikan = 'months-3'
        else:
            kikan = kikan.replace('年','').strip()
            kikan = f'year-{kikan}'

        driver.get(f'https://www.amazon.co.jp/gp/your-account/order-history?orderFilter={kikan}')
        elements = driver.find_elements_by_class_name("a-box.a-color-offset-background.order-info")
        if not elements:
        ## 自動ログインできない場合
            return False

        for i in range(0,1000,10):
            driver.get(f'https://www.amazon.co.jp/gp/your-account/order-history?orderFilter={kikan}&startIndex={i}')        
            elements = driver.find_elements_by_class_name("a-box.a-color-offset-background.order-info")

            if elements:
                for element in elements:
                    url = element.find_element_by_class_name('a-link-normal').get_attribute("href")
                    self._urls.append(url)
            else:
                break
        
        return True

    ### Amazonから購入履歴を取得してCSVファイルに保存する
    def toCsvPurchaseHistory(self,driver,kikan):
        startTime = com.getStartTime()
        logger.info('Amazonから購入履歴を取得してCSVファイルの作成開始')

        ## ログイン情報は、ユーザプロファイルに書き込む        
        ## 支払い明細のURL一覧を取得する
        ret = self.__getUrlList(driver,kikan)
        if not ret:
            return False
            
        ## 支払い明細から購入履歴を取得する
        datas = []
        count = 0
        for url in self._urls:
            flg = True
            driver.get(url)
            inners = driver.find_elements_by_class_name('a-fixed-left-grid-inner')
            for inner in inners:

                title = inner.find_elements_by_class_name('a-link-normal')[1].text
                if (title.find('Amazonギフト券') == -1) and (title.find('ダウンロード') == -1):
                ## Amazonギフト券チャージ、ダウンロード以外
                    count += 1
                    data = []
                    # 購入日
                    wrk = driver.find_elements_by_class_name('order-date-invoice-item')[0].text
                    wrk = wrk.replace('注文日','').strip()
                    data.append(wrk)
                    # 商品タイトル
                    data.append(title)
                    # 購入価格
                    wrk = inner.find_element_by_class_name('a-size-small.a-color-price').text
                    konyukakaku = wrk.replace('￥','').replace(',','').strip()
                    # 送料
                    if flg:
                    # 送料は1番目の商品のみ
                        flg = False                    
                        aRows = driver.find_element_by_id('od-subtotals').find_elements_by_class_name('a-row')
                        soryo = 0
                        waribiki = 0
                        for aRow in aRows:
                            wrk = aRow.text.split()
                            if len(wrk) > 0:
                                if wrk[0] == '配送料・手数料：':
                                    soryo = wrk[2].replace(',','').strip()
                                if wrk[0] == '割引：':
                                    waribiki = wrk[2].replace(',','').strip()
                        soryo = int(soryo) - int(waribiki)                    
                    else:
                        soryo = 0
                    data.append(int(konyukakaku) + soryo)
                    data.append(soryo)
                    # 出品者ID
                    wrk = inner.find_element_by_class_name('a-size-small.a-color-secondary').text
                    wrk = wrk.replace('販売:','').strip()
                    data.append(wrk)
                    datas.append(data)
                    # 取引ID
                    wrk = driver.find_elements_by_class_name('order-date-invoice-item')[1].text
                    wrk = wrk.strip().split()[1]
                    data.append(wrk)

        ## CSVファイルを作成する
        fileName = com.amazonFileName + f'({kikan})'
        com.toCsv(datas,fileName)

        endTime = com.getEndTime(startTime)        
        logger.info(f'Amazonから購入履歴を取得してCSVファイルの作成終了 >> {count}件取得 処理時間：{endTime} 秒')

        return True