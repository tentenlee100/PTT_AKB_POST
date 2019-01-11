import sys
import time
from PTTLibrary import PTT
import datetime
from config import *

KickOtherLogin = False

ID = PTT_ACCOUNT
Password = PTT_PASSWORD

PTTCrawler = PTT.Library(ID, Password, kickOtherLogin=False)
if not PTTCrawler.isLoginSuccess():
    PTTCrawler.Log('登入失敗')
    sys.exit()

# 這個範例是如何PO文
# 第一個參數是你要PO文的板
# 第二個參數是文章標題
# 第三個參數是文章內文
# 第四個參數是發文類別       1
# 第五個參數是簽名檔        	0
# 回傳值 就是錯誤碼
for i in range(1):
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d')
    title = '[LIVE] ' + st + ' Showroom+SNS直播 實況閒聊文'
    contents = '''
SR個別成員直播      https://www.showroom-live.com/campaign/akb48_sr \r\n
\r\n
概要: \r\n\r\n
除了成員各自showroom配信外，還有一些活動番組的showroom \r\n\r\n
大量開設instagram也會有個人的直播 \r\n\r\n
只要關於SNS的LIVE都可在這邊討論\r\n
\r\n
\r\n
showroom過濾網頁   https://tenten.tw/48showroom/\r\n
SR日飯製入口&分析站 http://sr48.net/\r\n
//停止使用中\r\n
\r\n
Instagram日飯製入口&分析站 http://ig48.gutas.net/\r\n
\r\n
twitter日飯製入口&分析站 http://tw48.net/\r\n
\r\n
TPE instagram彙整網站 https://tenten.tw/tpeig/ \r\n
\r\n
showroom 48 過濾 新工具: chrome extensions https://bit.ly/2HjQza9 \r\n
 類似之前的網頁版本，但是只有現在正在開播的清單。 \r\n
\r\n
'''

    ErrorCode = PTTCrawler.post('AKB48', title, contents, 0, 0)
    if ErrorCode == PTTCrawler.Success:
        PTTCrawler.Log('在 Test 板發文成功')
    elif ErrorCode == PTTCrawler.NoPermission:
        PTTCrawler.Log('發文權限不足')
    else:
        PTTCrawler.Log('在 Test 板發文失敗')
