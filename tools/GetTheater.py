import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict

from schedule import Stu


class GetTheater(object):
    AKB_IMG_NAME = 'cat_logo_akb48'
    SKE_IMG_NAME = 'cat_logo_ske48'
    NMB_IMG_NAME = 'cat_logo_nmb48'
    HKT_IMG_NAME = 'cat_logo_hkt48'
    NGT_IMG_NAME = 'cat_logo_ngt48'

    __THEATER_FORMAT__ : Dict[str, str] = {
        'AKB48': "\x15[1;35m╭─────╮\x15[m \r\n\x15[1;35m│AKB48 劇場│\x15[m {title} \r\n\x15[1;35m╰─────┴───────────────────────────────\x15[m \r\n",
        'SKE48': "\x15[1;33m╭─────╮\x15[m \r\n\x15[1;33m│SKE48 劇場│\x15[m {title} \r\n\x15[1;33m╰─────┴───────────────────────────────\x15[m \r\n",
        'NMB48': "\x15[1;32m╭─────╮\x15[m \r\n\x15[1;32m│NMB48 劇場│\x15[m {title} \r\n\x15[1;32m╰─────┴───────────────────────────────\x15[m \r\n",
        'HKT48': "\x15[1;36m╭─────╮\x15[m \r\n\x15[1;36m│HKT48 劇場│\x15[m {title} \r\n\x15[1;36m╰─────┴───────────────────────────────\x15[m \r\n",
        'NGT48': "\x15[1;31m╭─────╮\x15[m \r\n\x15[1;31m│NGT48 劇場│\x15[m {title} \r\n\x15[1;31m╰─────┴───────────────────────────────\x15[m \r\n",
        'STU48': "\x15[1;37m╭─────╮\x15[m \r\n\x15[1;37m│STU48 劇場│\x15[m {title} \r\n\x15[1;37m╰─────┴───────────────────────────────\x15[m \r\n",
    }

    def __init__(self):
        pass

    def _get_theater_info(self, element: BeautifulSoup) -> dict:
        return_dic = {
            'title': '休館日',
            'members': ''
        }
        a_tag = element.find('a')
        if a_tag is None:
            return return_dic

        detail_url = a_tag['href']
        title = a_tag.get_text().replace('\t', '').replace('\xa0', '').replace('\u3000', '').replace('\r', '').replace(
            '\n', '').replace('�U', 'Ⅱ').replace('�V', 'Ⅲ').replace('�W', 'Ⅳ')
        return_dic['title'] = title.split('開演:')[1] if title.split('開演:').__len__() > 1 else title
        return_dic['members'] = self._get_members(detail_url)
        return return_dic

    @staticmethod
    def _get_members(url: str) -> str:
        return_str = ''

        r = requests.get(url)
        s = BeautifulSoup(r.text, 'html.parser')
        detail_cont_box_list = s.find_all('div', 'detailContBox')

        for detail_cont_box in detail_cont_box_list:
            is_memeber_element = False
            for (index, child) in enumerate(detail_cont_box.find_all()):
                if index == 0 and 'メンバー' in child.get_text():
                    is_memeber_element = True
                    continue
                if is_memeber_element:
                    return_str = child.find().get_text().replace('\r\n', '\r\n\r\n').replace('※', '*').replace("��", "高").replace("�ｱ", "﨑")
                    is_memeber_element = False

        return return_str

    def get_schedule(self, query_date) -> dict:
        _query_date = datetime.strptime(query_date, "%Y/%m/%d")
        _query_date_string = _query_date.strftime("%Y-%m-%d")

        r = requests.get('https://ticket.akb48-group.com/home/event_live_list_dairy.php',
                         params={'date': _query_date_string})

        s = BeautifulSoup(r.text, 'html.parser')
        info_list = s.find('ul', 'infoList').find_all('li')

        # {
        #     'title': '休館日',
        #     'members': ''
        # }
        return_dic = {
            'AKB48': [],
            'SKE48': [],
            'NMB48': [],
            'HKT48': [],
            'NGT48': [],
        }

        for li in info_list:
            img_url = li.find('div', 'thumb').find('img')['src']
            if not img_url:
                continue
            if self.AKB_IMG_NAME in img_url:
                return_dic['AKB48'].append(self._get_theater_info(li))
            elif self.SKE_IMG_NAME in img_url:
                return_dic['SKE48'].append(self._get_theater_info(li))
            elif self.NMB_IMG_NAME in img_url:
                return_dic['NMB48'].append(self._get_theater_info(li))
            elif self.HKT_IMG_NAME in img_url:
                return_dic['HKT48'].append(self._get_theater_info(li))
            elif self.NGT_IMG_NAME in img_url:
                return_dic['NGT48'].append(self._get_theater_info(li))

        stu_list = Stu(query_date=query_date, theater=True).get_schedule()
        return_dic["STU48"] = [{"title":  stu.start_time + "〜" + stu.title , "members": '・'.join(stu.members)} for stu in stu_list]

        for key in return_dic.keys():
            if return_dic[key].__len__() == 0:
                return_dic[key].append({'title': '休館日', 'members': ''})


        return return_dic

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

if __name__ == '__main__':
    # query_date_str = datetime.today().strftime("%Y/%m/%d")
    query_date_str = '2019/04/20'
    # members = GetTheater().get_schedule(query_date_str)
    members = GetTheater().get_theater(query_date_str)
    print(members)
