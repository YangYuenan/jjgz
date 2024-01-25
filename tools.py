# -*- coding:utf-8 -*-

__author__ = 'yangyuenan'
__time__ = '2024/1/5 9:45'

import os
import yaml
from lxml import etree
import requests
from time import sleep


headers = {'User-Agent':
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}


def spider(code: str):
    info_url = 'https://www.dayfund.cn/fundpre/{code}.html'
    url = 'https://www.dayfund.cn/ajs/ajaxdata.shtml?showtype=getfundvalue&fundcode={code}'
    try:
        req = requests.get(url=url.format(code=code), headers=headers)
        jj_code = code
        jj_price = req.text.split('|')[7]
        jj_chg = req.text.split('|')[5]
        jj_time = req.text.split('|')[-2] + ' ' + req.text.split('|')[-1]
        req = requests.get(url=info_url.format(code=code), headers=headers)
        html = etree.HTML(req.text)
        jj_name = html.xpath('.//h1/text()')[0]
        return {'jj_code': jj_code, 'jj_name': jj_name, 'jj_price': jj_price, 'jj_chg': jj_chg, 'jj_time': jj_time}
    except Exception as e:
        return {}


def get_sz():
    sz_url = 'https://www.dayfund.cn/ajs/ajaxdata.shtml?showtype=getstockvalue&stockcode=sh000001,sz399001,sz399006,sh000300,sh000011&t=1004'
    try:
        req = requests.get(sz_url, headers=headers)
        sz = (req.text.split('深')[0].replace('上证指数', '上证指数：')
              .replace('span', 'font').replace('class', 'color'))
        return sz
    except Exception as e:
        return None


def init():
    jj_info = []
    if not os.path.exists('code.yml'):
        jj_code = {'code': jj_info}
        with open('code.yml', 'w', encoding='utf8')as f:
            yaml.dump(data=jj_code, stream=f, default_flow_style=False)
        return jj_info
    with open('code.yml', 'r', encoding='utf8')as f:
        jj_code = yaml.load(stream=f, Loader=yaml.FullLoader)
    if jj_code['code']:
        for code in jj_code['code']:
            result = spider(code)
            if result is None:
                return []
            jj_info.append(result)
                # sleep(0.5)
    return jj_info


def flush_conf(new_code):
    with open('code.yml', 'r', encoding='utf8')as f:
        jj_code = yaml.load(stream=f, Loader=yaml.FullLoader)
    jj_code['code'].append(new_code)
    with open('code.yml', 'w', encoding='utf8')as f:
        yaml.dump(data=jj_code, stream=f, default_flow_style=False)


def delete_code(index):
    with open('code.yml', 'r', encoding='utf8')as f:
        jj_code = yaml.load(stream=f, Loader=yaml.FullLoader)
    jj_code['code'].pop(index)
    with open('code.yml', 'w', encoding='utf8')as f:
        yaml.dump(data=jj_code, stream=f, default_flow_style=False)


if __name__ == '__main__':
    spider('013148')
