#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2019/6/26 14:36
'''
import json
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from furl import furl

from main.common import excel_util, time_util


def get_url(keywords, pn):
    page = {}
    s = quote(keywords)
    # &date = 4
    url = f"https://zhidao.baidu.com/search?&date=4&site=-1&sites=0&word={s}&pn={pn}"
    print(f"【get_url().url={url}】")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8"
    }
    data = requests.get(url, headers=headers)
    content = data.content
    soup = BeautifulSoup(content, 'html.parser')
    pager = soup.find(class_="pager")
    pager_last = pager.find(class_="pager-last")
    if pager_last:
        pager_last_url = pager_last["href"]
        last_pn = furl(pager_last_url).args['pn']
        page["last_pn"] = last_pn
    next_page = pager.find(class_="pager-next")
    if next_page:
        next_page_url = next_page["href"]
        next_pn = furl(next_page_url).args['pn']
        page["next_pn"] = next_pn
    else:
        page["next_pn"] = None

    current_pn = furl(url).args['pn']
    page["current_pn"] = current_pn

    html = soup.find(id="wgt-list").find_all("dl")
    items = []
    for i in html:
        item = {}
        find = i.find("dd", class_="dd explain f-light")
        find_all = find.find_all("span")
        if len(find_all) > 0:
            item['datetime'] = find_all[0].getText().strip()
        question = i.find("a").getText().strip()
        summary_find = i.find("dd", class_="dd summary")
        if summary_find:
            questionsummary = summary_find.getText().strip()
            if questionsummary:
                question = question + "\n" + questionsummary
        if question:
            item['question'] = question
        else:
            item['question'] = "无"
        answer = i.find("dd", class_="dd answer").getText().strip()
        if answer:
            item['answer'] = answer
        else:
            item['answer'] = "无"
        if len(find_all) > 1:
            item['answer_owner'] = find_all[1].getText().strip()
        else:
            item['answer_owner'] = "无"

        if len(find_all) > 2:
            item['other_answer'] = find_all[2].getText().strip()
        else:
            item['other_answer'] = "无"
        href_ = i.find("dt").find("a")["href"]
        if href_:
            item['href'] = href_.replace("&ie=gbk", "")
        else:
            item['href'] = "无"
        items.append(item)
    page['items'] = items
    return page


if __name__ == '__main__':
    pages = []
    items = []
    # keywords = "张家界景点推荐"
    # keywords = "一楼租房"
    # keywords = "租房平台推荐"
    # keywords = "民宿平台推荐"
    keywords ="租房推荐"
    page = {}
    page["next_pn"] = "0"
    while page["next_pn"]:
        try:
            page = get_url(keywords, page["next_pn"])
            pages.append(page)
        except Exception as e:
            print(f"{e}")
            next_pn = page["next_pn"]
            print(f"【main().next_pn={next_pn}】")

        print(f"【main().item={json.dumps(page, ensure_ascii=False, indent=4)}】")
        items_ = page['items']
        items.extend(items_)
        # time.sleep(5)
    date = time_util.now_to_date('%Y%m%d_%H%M')
    filename = date + keywords + "_baiduzhidao.xls"
    excel_util.write_excel(filename=filename, worksheet_name=date, items=items)
    print(f"【main().html=总共有{len(items)}条数据】")
    for item in items:
        post = requests.post("http://localhost:8080", json=item)
        print(f"【main().post={post}】")
