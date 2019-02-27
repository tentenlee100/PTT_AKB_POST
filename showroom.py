import sys
import time
from PTTLibrary import PTT
import datetime
from config import *
import os
import requests


class Showroom(object):

    @staticmethod
    def get_lang_schedule() -> str:
        contents = ""
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            team_tp_lang = ""
            r = requests.post('https://us-central1-akb48-tp.cloudfunctions.net/langSchedule', {"date": st}
                )
            json = r.json()
            if json is None or len(json) == 0:
                return team_tp_lang

            team_tp_lang += "" + "\r\n"
            team_tp_lang += "" + "\r\n"
            team_tp_lang += "本日Team TP 浪live 時程表 " + "\r\n"
            team_tp_lang += "" + "\r\n"

            for member in json:
                team_tp_lang += "{time} ({id}) {name}".format(time=member["time"], name=member["name"],id=member["lang"]) + "\r\n"

            team_tp_lang += "" + "\r\n"

            contents += team_tp_lang

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
        contents += "openrec 遊戲實況" + "\r\n"
        contents += "" + "\r\n"
        contents += "AKB48: https://www.openrec.tv/team/AKB48_official " + "\r\n"
        contents += "NMB48: https://www.openrec.tv/team/NMB48_official " + "\r\n"
        contents += "" + "\r\n"
        contents += "Instagram日飯製入口&分析站 http://ig48.gutas.net/" + "\r\n"
        contents += "" + "\r\n"
        contents += "twitter日飯製入口&分析站 http://tw48.net/" + "\r\n"
        contents += "" + "\r\n"
        contents += "AKE48 Team TP instagram彙整網站 https://tenten.tw/tpeig/        " + "\r\n"
        contents += "                   (有備份檔案) https://akb48-tp.tenten.tw/#/ig  " + "\r\n"
        contents += "" + "\r\n"
        contents += "showroom 48 過濾 新工具: chrome extensions https://bit.ly/2HjQza9" + "\r\n"
        contents += "" + "\r\n"

        contents += Showroom.get_lang_schedule()
        contents += "" + "\r\n"
        contents += "" + "\r\n"
        contents += "https://akb48-tp.tenten.tw/#/lang team tp 浪相關紀錄 " + "\r\n"


        return contents


if __name__ == '__main__':
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d')
    title = '[LIVE] ' + st + ' Showroom & 浪直播 實況閒聊文'
    contents = Showroom.get_content()

    print(contents)
    exit()
    ### 發文相關資訊填寫
    ID = PTT_ACCOUNT
    Password = PTT_PASSWORD
    board = 'TEST'
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
