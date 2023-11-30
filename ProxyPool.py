#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import csv
import time
import requests
import random
from bs4 import BeautifulSoup

# 存放代理池网址
urls = {'1': 'https://www.89ip.cn/',
        '2': 'http://www.ip3366.net/free/',
        '3': 'https://www.kuaidaili.com/free/'}

'''
网址及页码规则
url_1 = urls['1']+f'index_{page}.html'
url_2 = urls['2']+f'?stype=1&page={page}'
url_3 = urls['3']+f'intr/{page}/'
'''

# 配置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# 设置网站状态states为全局变量
global states

class ProxyPool:
    # 从89ip获取代理IP
    def GetProxy_89ip():
        proxies = []
        # 默认抓取第1-2页的IP
        pages = 2

        for page in range(0, pages):
            url = urls['1']+f'index_{str(page)}.html'
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", attrs={"class": "layui-table"})

            for row in table.tbody.find_all("tr"):
                cells = row.find_all("td")
                ip = cells[0].text.strip()
                port = cells[1].text.strip()

                # 89ip不显示协议,所以全部记为HTTP协议
                proxy = 'http://'+ip+':'+port
                if __name__ == '__main__':
                    print(proxy)

                proxies.append(proxy)
        return proxies

    # 从ip3366获取代理IP
    def GetProxy_ip3366():
        proxies = []
        # 默认抓取第1-1页的IP，获取后续页码内容时报错，有空再修
        pages = 1

        for page in range(0, pages):
            url = urls['2']+f'?stype=1&page={str(page)}'
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find(
                "table", attrs={"class": "table table-bordered table-striped"})

            for row in table.tbody.find_all("tr"):
                cells = row.find_all("td")
                ip = cells[0].text.strip()
                port = cells[1].text.strip()
                agreement = cells[3].text.strip()

                if agreement == 'HTTP':
                    proxy = 'http://'+ip+':'+port
                elif agreement == 'HTTPS':
                    proxy = 'https://'+ip+':'+port
                else:
                    proxy = agreement+'://'+ip+':'+port

                if __name__ == '__main__':
                    print(proxy)
                proxies.append(proxy)
        return proxies

    # 从kuaidaili获取代理IP
    def GetProxy_kuaidaili():
        proxies = []
        # 默认抓取第1-1页的IP，获取后续页码内容时报错，有空再修
        pages = 1+1

        for page in range(1, pages):
            url = urls['3']+f'intr/{str(page)}/'
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find(
                "table", attrs={"class": "table table-b table-bordered table-striped"})

            for row in table.tbody.find_all("tr"):
                cells = row.find_all("td")
                ip = cells[0].text.strip()
                port = cells[1].text.strip()
                agreement = cells[3].text.strip()
                if agreement == 'HTTP':
                    proxy = 'http://'+ip+':'+port
                elif agreement == 'HTTPS':
                    proxy = 'https://'+ip+':'+port
                else:
                    proxy = agreement+'://'+ip+':'+port

                if __name__ == '__main__':
                    print(proxy)
                proxies.append(proxy)
        return proxies

    # 测试代理池网址是否正常
    def TestProxyPool():
        begin_time = time.time()
        global states
        states = []
        for i in range(1, 4):
            try:
                response = requests.get(
                    url=urls[str(i)], headers=headers, timeout=100)
                if str(response) == '<Response [200]>':
                    states.append('可用')
            except:
                states.append('异常')

        end_time = time.time()
        time_used = end_time-begin_time
        return states, time_used


class Proxy:
    def TestProxy(proxies):
        os.system('cls')
        # 测试代理IP是否可用
        for i in range(len(proxies)):
            proxytest = {'test': proxies[i]}
            try:
                # 反正百度天天被爬，再添把火问题不大
                response = requests.get(
                    url='https://www.baidu.com/',
                    proxies=proxytest,
                    headers=headers,
                    timeout=100)
                print(proxies[i], '状态:可用', response)

            except:
                print(proxies[i], "失败",)


    def GetProxy(select):
        if select == '1':
            proxies = ProxyPool.GetProxy_89ip()
        elif select == '2':
            proxies = ProxyPool.GetProxy_ip3366()
        elif select == '3':
            proxies = ProxyPool.GetProxy_kuaidaili()
        Proxy.TestProxy(proxies)

        print('=====================================================')
        input('按Enter键继续')
        main('已初始化')


# 主界面
def main(mian):
    os.system('cls')
    print('=====================================================')
    print('         代理IP获取          作者：碧霄-凝落@Ninglog')
    print('    项目地址:https://github.com/BX-NL/ProxyPool')
    print('=====================================================')
    global states
    if mian == '未初始化':
        print(' 代理池初始化中。。。')
        states, time_used = ProxyPool.TestProxyPool()
        print(' 初始化完成!用时:', time_used)
        print('=====================================================')
    else:
        pass
    print(' 1. ', states[0], '仅HTTP     ', urls["1"])
    print(' 2. ', states[1], '少量HTTPS  ', urls["2"])
    print(' 3. ', states[2], '匿名度高   ', urls["3"])
    print(' 0. ', '退出')
    print('=====================================================')
    select = str(input(' 请选择代理池：'))
    print('=====================================================')
    if select == '1' or select == '2' or select == '3':
        Proxy.GetProxy(select)
    elif select == '0':
        # 没想到吧，这个退出选项实际上是个重启按钮
        os.system('cls')
        print(' 退出失败!')
        print()
        main('未初始化')
    else:
        print(' 请输入正确的数字')
        print()
        main('已初始化')


# 给其它程序留的接口,可获取一个可用的代理IP
def proxies(num=1):
    ram = random.randint(1,4)
    if ram == 1:
        proxies_full = ProxyPool.GetProxy_89ip()
    elif ram == 2:
        proxies_full = ProxyPool.GetProxy_ip3366()
    elif ram == 3:
        proxies_full = ProxyPool.GetProxy_kuaidaili()

    proxies = {}
    key = random.sample(range(0, len(proxies_full)), num)
    for i in range(num):
        proxies[str(i)] = proxies_full[key[i]]
    return proxies


# 保存所有可用的IP至文件
def save_proxies():

    with open('proxies.csv', 'w+', encoding='utf-8', newline='') as file:
        pass

if __name__ == '__main__':
    main('未初始化')
