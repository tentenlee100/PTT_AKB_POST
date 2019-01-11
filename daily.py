import sys
import time
from typing import Dict

from PTTLibrary import PTT
import datetime

from schedule import (
    Akb, Team8, Ske, Nmb, Hkt, Ngt, Stu
)
from birthday import GetBirthMember
from config import *

def add_title(contents, title):
    title_len = 0
    for s in title:
        if len(s) == len(s.encode()):
            if title_len + 1 < 80:
                title_len += 1
                contents += str(s)
            else:
                contents += "\r\n"
                title_len = 1
                contents += str(s)
        else:
            if title_len + 2 < 80:
                title_len += 2
                contents += str(s)
            else:
                contents += "\r\n"
                title_len = 2
                contents += str(s)
    contents += "\r\n"

    return contents


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

# 這個範例是如何PO文
# 第一個參數是你要PO文的板
# 第二個參數是文章標題
# 第三個參數是文章內文
# 第四個參數是發文類別       1
# 第五個參數是簽名檔        	0
# 回傳值 就是錯誤碼

st = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d')
title = '[閒聊] 本日行程與閒聊 ' + st
# title = '上色測試'

contents = ""
contents += "                                                                              " + "\r\n"
contents += "╭───────────────────────╮                             " + "\r\n"
contents += "│\x15[1;33m http://goo.gl/hKilDn            即時影音連結  \x15[m│                             " + "\r\n"
contents += "│\x15[1;33m https://akb48-bili.tenten.tw/   B站撈取網頁  \x15[m│                            " + "\r\n"
contents += "╰───────────────────────╯                             " + "\r\n"
contents += "\x15[1;43m                              \x15[40m■ \x15[33m歷史上的今天\x15[37m■\x15[43m                             \x15[m   " + "\r\n"
contents += "                                                                              " + "\r\n"

# 找生日成員
query_date = datetime.datetime.today().strftime("/%m/%d")
members = GetBirthMember().get_birth_member(query_date)

for member in members:
    group_format = __MEMBER_BIRTH_FORMAT__[member["group"]]
    contents += group_format.format(age=member["age"], name=member["name"])
    contents += " " + "\r\n"

contents += " " + "\r\n"
# 今日媒體行程
query_date = datetime.datetime.today().strftime("%Y/%m/%d")
contents += "\x15[1;46m                              \x15[40m■今日媒體行程■\x15[46m                            \x15[m    " + "\r\n"
contents += " " + "\r\n"
# AKB
contents += "\x15[1;35m◣\x15[37mAKB48\x15[35m◥├─────────────────────────────────\x15[m" + "\r\n"
contents += "\x15[1;35m╡\x15[37mメディア、イベント\x15[m" + "\r\n"

result = Akb(query_date).get_schedule()
for schedule in result:
    start_time = schedule.start_time
    if start_time.__len__() == 0:
        start_time = "     "
    line = "{start_time}  {title}".format(start_time=start_time, title=schedule.title)
    contents = add_title(contents, line)
# Team 8
result = Team8(query_date).get_schedule()
for schedule in result:
    start_time = schedule.start_time
    if start_time.__len__() == 0:
        start_time = "     "
    line = "{start_time}  {title}".format(start_time=start_time, title=schedule.title)
    contents = add_title(contents, line)
# Ske
contents += " " + "\r\n"
contents += "\x15[1;33m◣\x15[37mSKE48\x15[33m◥├─────────────────────────────────\x15[m" + "\r\n"
contents += "\x15[1;33m╡\x15[37mメディア、イベント\x15[m" + "\r\n"

result = Ske(query_date).get_schedule()
for schedule in result:
    start_time = schedule.start_time
    if start_time.__len__() == 0:
        start_time = "     "
    line = "{start_time}  {title}".format(start_time=start_time, title=schedule.title)
    contents = add_title(contents, line)
# Nmb
contents += " " + "\r\n"
contents += "\x15[1;32m◣\x15[37mNMB48\x15[32m◥├─────────────────────────────────\x15[m" + "\r\n"
contents += "\x15[1;32m╡\x15[37mメディア、イベント\x15[m" + "\r\n"

result = Nmb(query_date).get_schedule()
for schedule in result:
    start_time = schedule.start_time
    if start_time.__len__() == 0:
        start_time = "     "
    line = "{start_time}  {title}".format(start_time=start_time, title=schedule.title)
    contents = add_title(contents, line)

# HKT
contents += " " + "\r\n"
contents += "\x15[1;36m◣\x15[37mHKT48\x15[36m◥├─────────────────────────────────\x15[m" + "\r\n"
contents += "\x15[1;36m╡\x15[37mメディア、イベント\x15[m" + "\r\n"

result = Hkt(query_date).get_schedule()
for schedule in result:
    start_time = schedule.start_time
    if start_time.__len__() == 0:
        start_time = "     "
    line = "{start_time}  {title}".format(start_time=start_time, title=schedule.title)
    contents = add_title(contents, line)

# NGT
contents += " " + "\r\n"
contents += "\x15[1;31m◣\x15[37mNGT48\x15[31m◥├─────────────────────────────────\x15[m" + "\r\n"
contents += "\x15[1;31m╡\x15[37mメディア、イベント\x15[m" + "\r\n"

result = Ngt(query_date).get_schedule()
for schedule in result:
    start_time = schedule.start_time
    if start_time.__len__() == 0:
        start_time = "     "
    line = "{start_time}  {title}".format(start_time=start_time, title=schedule.title)
    contents = add_title(contents, line)

# STU
contents += " " + "\r\n"
contents += "\x15[1;34m◣\x15[37mSTU48\x15[34m◥├─────────────────────────────────\x15[m" + "\r\n"
contents += "\x15[1;34m╡\x15[37mメディア、イベント\x15[m" + "\r\n"

result = Stu(query_date).get_schedule()
for schedule in result:
    start_time = schedule.start_time
    if start_time.__len__() == 0:
        start_time = "     "
    line = "{start_time}  {title}".format(start_time=start_time, title=schedule.title)
    contents = add_title(contents, line)

print(contents)

KickOtherLogin = False

ID = PTT_ACCOUNT
Password = PTT_PASSWORD

PTTBot = PTT.Library(kickOtherLogin=False)

ErrCode = PTTBot.login(ID, Password)
if ErrCode != PTT.ErrorCode.Success:
    PTTBot.Log('登入失敗')
    sys.exit()

# ErrorCode = PTTCrawler.post('AKB48', title, contents, 0, 0)
# if ErrorCode == PTTCrawler.Success:
#     PTTCrawler.Log('在 Test 板發文成功')
#     PTTCrawler.throwWaterBall('emperor', '測試 今日閒聊文已發文')
#
# elif ErrorCode == PTTCrawler.NoPermission:
#     PTTCrawler.Log('發文權限不足')
# else:
#     PTTCrawler.Log('在 Test 板發文失敗')

PTTBot.throwWaterBall('emperor', '測試 今日閒聊文已發文')


PTTBot.logout()
