# -*- coding: utf-8 -*-

# python3.6
# 抓取今日头条街拍图 2018/8/26
# https://cuiqingcai.com/5616.html

import json
import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool

def get_page(offset):
    params = {
        'offset':offset,
        'format':'json',
        'keyword':'街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) '
                      + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.ConnectionError:
        return None


def get_image(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('image_list'):
                title = item.get('title')
                images = item.get('image_list')
                for image in images:
                    yield {
                        'image':'http:'+ image.get('url'),
                        'title':title
                    }

def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('file exists ', file_path)
    except requests.ConnectionError:
        print('failded to save image')

def main(offset):
    json = get_page(offset)
    for item in get_image(json):
        print(item)
        save_image(item)

# main(20)

GROUP_START = 1
GROUP_END = 2

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()









