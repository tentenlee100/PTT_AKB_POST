import sys
import time
from PTTLibrary import PTT
import datetime
from config import *
import os


class Showroom(object):

    @staticmethod
    def get_lang_schedule() -> str:
        contents = ""
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            team_tp_lang =""
            dir_path = os.path.join(dir_path, "team_tp_lang")
            file_path = os.path.join(dir_path, st + ".txt")
            print(file_path)
            file = open(file_path, "r", encoding="utf-8")
            text = file.read().replace("\n", "\r\n")

            team_tp_lang += "" + "\r\n"
            team_tp_lang += "" + "\r\n"
            team_tp_lang += "本日Team TP 浪live 時程表 " + "\r\n"
            team_tp_lang += "" + "\r\n"
            team_tp_lang += text + "\r\n"
            team_tp_lang += "" + "\r\n"

            contents += team_tp_lang
            print(repr(text))
        except Exception as e:
            print("caught", repr(e))

        return contents

    @staticmethod
    def get_content() -> str:
        contents = ""
        contents += "SR個別成員直播      https://www.showroom-live.com/campaign/akb48_sr" + "\r\n"
        contents += "" + "\r\n"
        contents += "概要:" + "\r\n"
        contents += "" + "\r\n"
        contents += "除了成員各自showroom配信外，還有一些活動番組的showroom" + "\r\n"
        contents += "" + "\r\n"
        contents += "大量開設instagram也會有個人的直播" + "\r\n"
        contents += "" + "\r\n"
        contents += "只要關於SNS的LIVE都可在這邊討論" + "\r\n"
        contents += "" + "\r\n"
        contents += "showroom過濾網頁   https://tenten.tw/48showroom/" + "\r\n"
        contents += "" + "\r\n"
        contents += "" + "\r\n"
        contents += "Instagram日飯製入口&分析站 http://ig48.gutas.net/" + "\r\n"
        contents += "" + "\r\n"
        contents += "twitter日飯製入口&分析站 http://tw48.net/" + "\r\n"
        contents += "" + "\r\n"
        contents += "AKE48 TeamTP instagram彙整網站 https://tenten.tw/tpeig/" + "\r\n"
        contents += "" + "\r\n"
        contents += "showroom 48 過濾 新工具: chrome extensions https://bit.ly/2HjQza9" + "\r\n"
        contents += "" + "\r\n"

        contents += Showroom.get_lang_schedule()

        return contents


if __name__ == '__main__':
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d')
    title = '[LIVE] ' + st + ' Showroom+SNS直播 實況閒聊文'
    contents = Showroom.get_content()

    print(contents)

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

    ErrorCode = PTTBot.post(board, title, contents, 0, 0)
    if ErrorCode == PTT.ErrorCode.Success:
        PTTBot.Log('在' + board + '板發文成功')

    elif ErrorCode == PTT.ErrorCode.NoPermission:
        PTTBot.Log('發文權限不足')
    else:
        PTTBot.Log('在 Test 板發文失敗')

    PTTBot.logout()
