import sys
import time
from typing import Dict

from PTTLibrary import PTT
import datetime

from schedule import (
    Akb, Team8, Ske, Nmb, Hkt, Ngt, Stu
)
from tools import (GetBirthMember, GetTheater, GetVideo)
from config import *


def add_title(_contents, _title):
    title_len = 0
    for s in _title:
        if len(s) == len(s.encode()):
            if title_len + 1 < 80:
                title_len += 1
                _contents += str(s)
            else:
                _contents += "\r\n"
                title_len = 1
                _contents += str(s)
        else:
            if title_len + 2 < 80:
                title_len += 2
                _contents += str(s)
            else:
                _contents += "\r\n"
                title_len = 2
                _contents += str(s)
    _contents += "\r\n"

    return _contents


def add_content_one_line(_title):
    title_len = 0
    _contents = ""
    for s in _title:
        if len(s) == len(s.encode()):
            if title_len + 1 < 80:
                title_len += 1
                _contents += str(s)
            else:
                _contents += "\r\n"
                title_len = 1
                _contents += str(s)
        else:
            if title_len + 2 < 80:
                title_len += 2
                _contents += str(s)
            else:
                _contents += "\r\n"
                title_len = 2
                _contents += str(s)
    _contents += "\r\n"

    return _contents


class Daily(object):
    __MEMBER_BIRTH_FORMAT__: Dict[str, str] = {
        'AKB48': "\x15[1;37m＊ \x15[35mAKB48      \x15[37m  ({age})  {name}\x15[m",
        'SKE48': "\x15[1;37m＊ \x15[33mSKE48      \x15[37m  ({age})  {name}\x15[m",
        'NMB48': "\x15[1;37m＊ \x15[32mNMB48      \x15[37m  ({age})  {name}\x15[m",
        'HKT48': "\x15[1;37m＊ \x15[36mHKT48      \x15[37m  ({age})  {name}\x15[m",
        'NGT48': "\x15[1;37m＊ \x15[31mNGT48      \x15[37m  ({age})  {name}\x15[m",
        'STU48': "\x15[1;37m＊ \x15[34mSTU48      \x15[37m  ({age})  {name}\x15[m",
        'BNK48': "\x15[1;37m＊ \x15[0;35mBNK48      \x15[1;37m  ({age})  {name}\x15[m",
        'AKB48 TeamTP': "\x15[1;37m＊ \x15[33mAKB48 TeamTP\x15[37m ({age})  {name}\x15[m",
    }

    __THEATER_FORMAT__: Dict[str, str] = {
        'AKB48': "\x15[1;35m╭─────╮\x15[m \r\n\x15[1;35m│AKB48 劇場│\x15[m {title} \r\n\x15[1;35m╰─────┴───────────────────────────────\x15[m \r\n",
        'SKE48': "\x15[1;33m╭─────╮\x15[m \r\n\x15[1;33m│SKE48 劇場│\x15[m {title} \r\n\x15[1;33m╰─────┴───────────────────────────────\x15[m \r\n",
        'NMB48': "\x15[1;32m╭─────╮\x15[m \r\n\x15[1;32m│NMB48 劇場│\x15[m {title} \r\n\x15[1;32m╰─────┴───────────────────────────────\x15[m \r\n",
        'HKT48': "\x15[1;36m╭─────╮\x15[m \r\n\x15[1;36m│HKT48 劇場│\x15[m {title} \r\n\x15[1;36m╰─────┴───────────────────────────────\x15[m \r\n",
        'NGT48': "\x15[1;31m╭─────╮\x15[m \r\n\x15[1;31m│NGT48 劇場│\x15[m {title} \r\n\x15[1;31m╰─────┴───────────────────────────────\x15[m \r\n",
        'STU48': "\x15[1;37m╭─────╮\x15[m \r\n\x15[1;37m│STU48 劇場│\x15[m {title} \r\n\x15[1;37m╰─────┴───────────────────────────────\x15[m \r\n",
    }

    __SCHEDULE_TITLE_FORMAT__: Dict[str, str] = {
        'AKB48': "\x15[1;35m◣\x15[37mAKB48\x15[35m◥├─────────────────────────────────\x15[m\r\n\x15[1;35m╡\x15[37mメディア、イベント\x15[m\r\n",
        'SKE48': "\x15[1;33m◣\x15[37mSKE48\x15[33m◥├─────────────────────────────────\x15[m\r\n\x15[1;33m╡\x15[37mメディア、イベント\x15[m\r\n",
        'NMB48': "\x15[1;32m◣\x15[37mNMB48\x15[32m◥├─────────────────────────────────\x15[m\r\n\x15[1;32m╡\x15[37mメディア、イベント\x15[m\r\n",
        'HKT48': "\x15[1;36m◣\x15[37mHKT48\x15[36m◥├─────────────────────────────────\x15[m\r\n\x15[1;36m╡\x15[37mメディア、イベント\x15[m\r\n",
        'NGT48': "\x15[1;31m◣\x15[37mNGT48\x15[31m◥├─────────────────────────────────\x15[m\r\n\x15[1;31m╡\x15[37mメディア、イベント\x15[m\r\n",
        'STU48': "\x15[1;34m◣\x15[37mSTU48\x15[34m◥├─────────────────────────────────\x15[m\r\n\x15[1;34m╡\x15[37mメディア、イベント\x15[m\r\n",
    }

    def get_birth(self) -> str:
        contents = ""

        # 找生日成員
        query_date = datetime.datetime.today().strftime("/%m/%d")
        members = GetBirthMember().get_birth_member(query_date)

        for member in members:
            group_format = self.__MEMBER_BIRTH_FORMAT__[member["group"]]
            contents += group_format.format(age=member["age"], name=member["name"])
            contents += " " + "\r\n"

        contents += " " + "\r\n"
        return contents

    def get_schedule(self, group: str, query_date: str) -> str:
        contents = ""
        contents += self.__SCHEDULE_TITLE_FORMAT__[group]
        contents += " " + "\r\n"

        run_class_object = []

        if group == 'AKB48':
            run_class_object = [Akb(query_date), Team8(query_date)]
        elif group == 'SKE48':
            run_class_object = [Ske(query_date)]
        elif group == 'NMB48':
            run_class_object = [Nmb(query_date)]
        elif group == 'HKT48':
            run_class_object = [Hkt(query_date)]
        elif group == 'NGT48':
            run_class_object = [Ngt(query_date)]
        elif group == 'STU48':
            run_class_object = [Stu(query_date)]

        for group_class_object in run_class_object:
            result = group_class_object.get_schedule()
            for schedule in result:
                start_time = schedule.start_time
                if start_time.__len__() == 0:
                    start_time = "     "
                line = "{start_time}  {title}".format(start_time=start_time, title=schedule.title)
                contents += add_content_one_line(line)

        return contents

    def get_theater(self, query_date: str) -> str:
        contents = ""
        theater_list = GetTheater().get_schedule(query_date)

        for theater in theater_list.keys():
            for event in theater_list[theater]:
                group_format = self.__THEATER_FORMAT__[theater]
                contents += group_format.format(title=event["title"])
                contents += add_content_one_line(event["members"])
                contents += " " + "\r\n"

        return contents

    def get_video(self) -> str:
        contents = ""
        video_list = GetVideo().get_video()
        video_title_format = '\x15[1;33m{title}\x15[m\r\n\r\n'

        for type in video_list:
            contents += video_title_format.format(title=type['title'])
            for links in type['links']:
                for links_detail in links:
                    contents += add_content_one_line(links_detail)
                contents += " " + "\r\n"
            contents += " " + "\r\n"
        return contents

    def get_content(self) -> str:

        contents = ""
        contents += "                                                                              " + "\r\n"
        contents += "╭───────────────────────╮                             " + "\r\n"
        contents += "│\x15[1;33m http://goo.gl/hKilDn            即時影音連結  \x15[m│                             " + "\r\n"
        contents += "│\x15[1;33m https://akb48-bili.tenten.tw/   B站撈取網頁  \x15[m│                            " + "\r\n"
        contents += "╰───────────────────────╯                             " + "\r\n"
        contents += "                              https://bit.ly/2M9ATbS 程式開源 有需要可自取" + "\r\n"
        contents += "                                                                              " + "\r\n"

        # 歷史上的今天 成員生日
        contents += "\x15[1;43m                              \x15[40m■ \x15[33m歷史上的今天\x15[37m■\x15[43m                             \x15[m   " + "\r\n"
        contents += "                                                                              " + "\r\n"
        contents += self.get_birth()

        # 今日媒體行程
        query_date = datetime.datetime.today().strftime("%Y/%m/%d")
        contents += "\x15[1;46m                              \x15[40m■今日媒體行程■\x15[46m                            \x15[m    " + "\r\n"
        contents += " " + "\r\n"

        for key in self.__SCHEDULE_TITLE_FORMAT__.keys():
            contents += self.get_schedule(key, query_date)
            contents += " " + "\r\n"

        # 找劇場
        contents += " " + "\r\n"
        contents += " " + "\r\n"
        contents += " " + "\r\n"
        contents += "\x15[1;42m                              \x15[40m■劇場公演情報■\x15[42m                              \x15[m" + "\r\n"
        contents += " " + "\r\n"

        contents += self.get_theater(query_date)

        # 找影音連結
        contents += " " + "\r\n"
        contents += " " + "\r\n"
        contents += " " + "\r\n"
        contents += "\x15[1;44m                              \x15[40m■影音連結整理■\x15[44m                              \x15[m" + "\r\n"
        contents += " " + "\r\n"
        contents += " " + "\r\n"

        contents += self.get_video()
        contents += " " + "\r\n"
        contents += "※ 影音整理：fatetree  \r\n"

        return contents


if __name__ == '__main__':
    st = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d')
    title = '[閒聊] 本日行程與閒聊 ' + st
    contents = Daily().get_content()

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
        PTTBot.throwWaterBall('emperor', '今日閒聊文已發文')

    elif ErrorCode == PTT.ErrorCode.NoPermission:
        PTTBot.Log('發文權限不足')
    else:
        PTTBot.Log('在 Test 板發文失敗')

    PTTBot.logout()
