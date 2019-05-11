import sys
import time
from daily import *
from showroom import *
from typing import Dict

from PTTLibrary import PTT
import datetime

from config import *


if __name__ == '__main__':

    # 發送showroom文
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d')
    showroom_title = '[LIVE] ' + st + ' Showroom & 浪直播 實況閒聊文'
    showroom_contents = Showroom.get_content()
    print(showroom_contents)

    ### 發文相關資訊填寫
    ID = PTT_ACCOUNT
    Password = PTT_PASSWORD
    board = 'AKB48'
    KickOtherLogin = False
    ###
    PTTBot = PTT.Library(kickOtherLogin=KickOtherLogin)

    ErrCode = PTTBot.login(ID, Password)
    if ErrCode != PTT.ErrorCode.Success:
        PTTBot.Log('登入失敗')
        sys.exit()

    ErrorCode = PTTBot.post(board, showroom_title, showroom_contents, 0, 0)
    if ErrorCode == PTT.ErrorCode.Success:
        PTTBot.Log('在' + board + '板發SHOWROOM文成功')

    elif ErrorCode == PTT.ErrorCode.NoPermission:
        PTTBot.Log('發文權限不足')
    else:
        PTTBot.Log('在 Test 板發文失敗')

    # 發送每日文
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d')
    daily_title = '[閒聊] 本日行程與閒聊 ' + st
    daily_contents = Daily().get_content()
    print(daily_contents)

    for i in range(3):
        ErrorCode = PTTBot.post(board, daily_title, daily_contents, 0, 0)
        if ErrorCode == PTT.ErrorCode.Success:
            PTTBot.Log('在' + board + '板今日閒聊文發文成功')
            if board == 'AKB48':
                PTTBot.throwWaterBall('emperor', '今日閒聊文已發文')
            break
        elif ErrorCode == PTT.ErrorCode.NoPermission:
            PTTBot.Log('發文權限不足')
        else:
            PTTBot.Log('在 Test 板發文失敗')

    PTTBot.logout()