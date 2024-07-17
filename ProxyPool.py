#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import time
import random
import requests
from lxml import etree
from bs4 import BeautifulSoup

# 存放代理池网址及其编号
urls = {
    '1': 'https://www.89ip.cn/',
    '2': 'http://www.ip3366.net/free/',
    '3': 'https://www.kuaidaili.com/free/',
}

# 配置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

states = ['未测试', '未测试', '未测试'] # 设置网站初始状态
mian = '未初始化' # 设置程序初始化状态mian，检测main()是否第一次启动


class ProxyPool: # 定义ProxyPool类

    def GetProxyPoolSource(url): # 传入网址，获取网页源码。闲着没事干，就算只有两行也要写个函数
        response = requests.get(url=url, headers=headers) # 使用requests发送GET请求
        source = BeautifulSoup(response.content, 'html.parser') # 使用bs4解析网页源码   
        return source # 返回网页源码
    
    class ProxyPool_89ip: # 定义89ip类

        def GetProxy_89ip_IP(): # 从89ip获取代理IP
            proxies_list = [] # 定义列表用于保存IP
            pages = 1 # 接口模式下默认只获取第1页的IP

            for page in range(0, pages): # 遍历每一页的内容
                url = urls['1'] + f'index_{str(page)}.html' # 设置对应页码的网址
                source = ProxyPool.GetProxyPoolSource(url) #  获取网页源码
                table = source.find('table', attrs={'class': 'layui-table'}) # 定位目标表格

                for row in table.tbody.find_all('tr'): # 遍历表格每一行内容
                    cells = row.find_all('td') # 定位每行所有元素
                    ip = cells[0].text.strip() # 获取IP地址
                    port = cells[1].text.strip() # 获取端口

                    proxy = 'http' + '://' + ip + ':' + port # 89ip不显示协议,所以全部记为HTTP协议
                    proxies_list.append(proxy) # 保存每个IP

            return proxies_list
        
        def GetProxy_89ip_Info(): # 从89ip获取信息
            proxies_info = [] # 定义列表用于保存信息
            pages = 6 # 全量模式下默认获取第1~6页的数据
            for page in range(0, pages): # 遍历每一页的内容
                print('正在获取第', page+1, '页') # 向控制台打印页码
                url = urls['1'] + f'index_{str(page)}.html' # 设置对应页码的网址
                source = ProxyPool.GetProxyPoolSource(url) # 获取网页源码
                table = source.find('table', attrs={'class': 'layui-table'}) # 定位目标表格

                html = etree.HTML(str(source)) # 用lxml解析网页
                title = html.findtext('.//title') # 获取完整网页标题，什么大聪明把<title>写<body>里，xpath找半天不如直接findtext
                title = re.search('[^_]+$', title).group() # 正则表达式修改网页标题

                for row in table.tbody.find_all('tr'): # 遍历表格每一行内容
                    cells = row.find_all('td') # 定位每行所有元素
                    ip = cells[0].text.strip() # 获取IP地址
                    port = cells[1].text.strip() # 获取端口
                    location = cells[2].text.strip() # 获取代理位置
                    operator = cells[3].text.strip() # 获取运营商
                    date = cells[4].text.strip() # 获取时间

                    proxies_info.append([title, 'HTTP', ip, port, location, operator, date]) # 记录每行信息

                time.sleep(3) # 晚安玛卡巴卡

            return proxies_info
        
    class ProxyPool_ip3366: # 定义ip3366类

        def GetProxy_ip3366_IP(): # 从ip3366获取代理IP
            proxies_list = [] # 定义列表用于保存IP
            pages = 1 # 接口模式下默认获取第1-1页的IP，获取后续页码内容时错误，修不了

            for page in range(0, pages): # 遍历每一页的内容
                url = urls['2'] + f'?stype=1&page={str(page)}' # 设置网址
                source = ProxyPool.GetProxyPoolSource(url) # 获取网页源码
                table = source.find('table', attrs={'class': 'table table-bordered table-striped'}) # 定位指定表格

                for row in table.tbody.find_all('tr'): # 遍历表格每一行内容
                    cells = row.find_all('td') # 定位每行所有元素
                    ip = cells[0].text.strip() # 获取IP地址
                    port = cells[1].text.strip() # 获取端口
                    agreement = cells[3].text.strip() # 获取代理协议

                    proxy = agreement.lower() + '://' + ip + ':' + port # 代理IP=协议(小写)+ip+端口
                    proxies_list.append(proxy) # 保存每个IP

            return proxies_list
        
        def GetProxy_ip3366_Info(): # 从ip3366获取信息
            proxies_info = [] # 定义列表用于保存信息
            pages = 1 # 全量模式下默认抓取第1-1页的数据，获取后续页码内容时错误，修不了

            for page in range(0, pages): # 遍历每一页的内容
                print('正在获取第', page+1, '页') # 向控制台打印页码
                url = urls['2'] + f'?stype=1&page={str(page)}' # 设置网址
                source = ProxyPool.GetProxyPoolSource(url) # 获取网页源码
                table = source.find('table', attrs={'class': 'table table-bordered table-striped'}) # 定位指定表格

                html = etree.HTML(str(source)) # 用lxml解析网页
                title = html.xpath('/html/head/title')[0].text # 使用XPath获取完整标题
                title = re.sub('\s.+$', '', title) # 正则表达式修改网页标题

                for row in table.tbody.find_all('tr'): # 遍历表格每一行内容
                    cells = row.find_all('td') # 定位每行所有元素
                    ip = cells[0].text.strip() # 获取IP地址
                    port = cells[1].text.strip() # 获取端口
                    agreement = cells[3].text.strip() # 获取代理协议
                    location_operator = cells[4].text.strip() # 获取代理位置和运营商，格式:	高匿_XX省XX市XXX
                    try:
                        location_operator = re.sub('高匿_', '', location_operator) # 正则表达式去除'高匿_'
                    except:
                        pass # 什么垃圾网站，做个表格连格式都不统一
                    try:
                        location = re.search('(^.+(?<=市))|(^.+(?<=国))', location_operator).group() # 正则表达式匹配代理位置
                    except:
                        location = location_operator # 找不到代理位置就寄
                    try:
                        operator = re.search('((?<=市).+)|((?<=国).+)', location_operator).group() # 正则表达式匹配运营商
                    except:
                        operator = 'None' # 找不到运营商就设置为空
                    date = cells[6].text.strip() # 获取时间

                    proxies_info.append([title, agreement, ip, port, location, operator, date]) # 记录每行信息

                time.sleep(3) # 晚安玛卡巴卡

            return proxies_info
           
    class ProxyPool_kuaidaili: # 定义kuaidaili类

        def GetProxy_kuaidaili_IP(): # 从kuaidaili获取代理IP

            proxies_list = [] # 定义列表用于保存IP
            pages = 1 # 接口模式下默认获取第1-1页的IP，获取后续页码内容时报错，有空再修

            for page in range(1, pages+1): # 遍历每一页的内容
                url = urls['3'] + f'intr/{str(page)}/' # 设置对应页码的网址:普通开放
                # url = urls['3'] + f'inha/{str(page)}/' # 设置对应页码的网址:高匿开放
                source = ProxyPool.GetProxyPoolSource(url) # 获取网页源码
                table = source.find('table', attrs={'class': 'table table-b table-bordered table-striped'}) # 定位指定表格
                for row in table.tbody.find_all('tr'): # 遍历表格每一行内容
                    cells = row.find_all('td') # 定位每行所有元素
                    ip = cells[0].text.strip() # 获取IP地址
                    port = cells[1].text.strip() # 获取端口
                    agreement = cells[3].text.strip() # 获取代理协议

                    proxy = agreement.lower() + '://' + ip + ':' + port # 代理IP=协议(小写)+ip+端口
                    proxies_list.append(proxy) # 保存每个IP
                time.sleep(5) # 晚安玛卡巴卡

            return proxies_list
        
        def GetProxy_kuaidaili_Info(): # 从kuaidaili获取信息

            proxies_info = [] # 定义列表用于保存信息
            pages = 10 # 全量模式下默认获取第1-10页的信息。获取后续页码内容时如果报错就把下面的sleep改大

            for page in range(1, pages+1): # 遍历每一页的内容
                print('正在获取第', page, '页') # 向控制台打印页码
                url = urls['3'] + f'intr/{str(page)}/' # 设置对应页码的网址:普通开放
                # url = urls['3'] + f'inha/{str(page)}/' # 设置对应页码的网址:高匿开放
                source = ProxyPool.GetProxyPoolSource(url) # 获取网页源码
                table = source.find('table', attrs={'class': 'table table-b table-bordered table-striped'}) # 定位指定表格
                title = source.title.string # 好烦啊不想用lxml了
                title = re.search('[^-\s]+$', title).group() # 正则表达式修改网页标题

                for row in table.tbody.find_all('tr'): # 遍历表格每一行内容
                    cells = row.find_all('td') # 定位每行所有元素
                    ip = cells[0].text.strip() # 获取IP地址
                    port = cells[1].text.strip() # 获取端口
                    agreement = cells[3].text.strip() # 获取代理协议
                    location_operator = cells[4].text.strip() # 获取代理位置和运营商，格式:XX国 XX XX XX或XX省XX市 XX
                    operator = re.search('([^\s]+)$', location_operator).group() # 获取运营商
                    location = re.sub(operator, '', location_operator) # 正则表达式匹配运营商并删除
                    location = re.sub('\s', '', location) # 正则表达式删除空格以获取代理位置
                    date = cells[6].text.strip() # 获取时间
                    date = re.sub('-', '/', date) # 使用正则表达式格式化时间

                    proxies_info.append([title, agreement, ip, port, location, operator, date]) # 记录每行信息

                time.sleep(5) # 晚安玛卡巴卡
            return proxies_info

    # 测试代理池网址是否正常
    def TestProxyPool():
        begin_time = time.time() # 开始记录时间
        global states # 设置网站状态为全局变量
        for i in range(1, 4): # 遍历所有网址
            try:
                response = requests.get(url=urls[str(i)], headers=headers, timeout=100) # 向网站发送请求，默认超时时间为100
                if str(response) == '<Response [200]>': # 判断网站是否可以访问
                    states[i-1] = ('可用') # 记录网站状态
            except:
                states[i-1] = ('异常') # 记录网站状态

        end_time = time.time() # 记录结束时间
        time_used = end_time - begin_time # 统计用时
        return time_used


class Proxy:

    def TestProxy(proxies): # 测试代理IP是否可用
        global mian
        for i in range(len(proxies)): # 遍历所有IP
            agreement = re.search('https|http', proxies[str(i)]).group() # 获取代理IP的协议
            agreement = agreement.upper() # 将协议转为大写，作为键值
            proxies_test = {'HTTP' : proxies[str(i)]} # 配置代理IP

            try:
                # 反正百度天天被爬，再添把火问题不大
                response = requests.get(
                    url='https://www.baidu.com/',
                    proxies=proxies_test,
                    headers=headers,
                    timeout=1,
                )
                proxty_status = '状态:可用' # 记录代理IP状态
            except:
                proxty_status = '失败' # 记录代理IP状态
                # del proxies[str[i]] # 移除不可用的IP，接口模式下工作不正常，暂时注释
            
            # time.sleep(1) # 晚安，玛卡巴卡
            if mian == '已初始化': # 判断是否作为主程序在执行 
                print(proxies[str(i)], proxty_status, response) # 向控制台输出IP与测试结果
        return proxies


    def TestProxy_True(proxies): # 测试代理IP是否可用(真实版)，九个IP有十个不能用
        global mian
        for i in range(len(proxies)): # 遍历所有IP
            agreement = re.search('https|http', proxies[str(i)]).group() # 获取代理IP的协议
            agreement = agreement.upper() # 将协议转为大写，作为键值
            proxies_test = {'HTTP' : proxies[str(i)]} # 配置代理IP # 协议默认HTTP，HTTPS有点毛病

            try:
                # 发送请求到这个网址会返回IP
                response = requests.get(
                    url='http://icanhazip.com/',
                    proxies=proxies_test,
                    headers=headers,
                    timeout=200,
                )
                # print(response.text) # 全是返回的本机真实IP，修个锤子
                if 'http://'+response.text == proxies_test['HTTP']: # 检测返回的IP与代理IP是否相等
                    proxty_status = '状态:可用' # 记录代理IP状态
                else:
                    proxty_status = '失败' # 记录代理IP状态
            except:
                proxty_status = '失败' # 记录代理IP状态
            # del proxies[str[i]] # 移除不可用的IP，接口模式下工作不正常，暂时注释
            
            # time.sleep(1) # 晚安，玛卡巴卡
            if mian == '已初始化': # 判断是否作为主程序在执行 
                print(proxies[str(i)], proxty_status, response) # 向控制台输出IP与测试结果
        return proxies

    def GetProxy(select):
        # 用字典记录需要调用的函数，Python没有switch/case好麻烦
        proxies_dict = {
            '1' : ProxyPool.ProxyPool_89ip.GetProxy_89ip_IP,
            '2' : ProxyPool.ProxyPool_ip3366.GetProxy_ip3366_IP,
            '3' : ProxyPool.ProxyPool_kuaidaili.GetProxy_kuaidaili_IP
        }
        proxies_list = proxies_dict[str(select)]() # 调用函数获取IP，
        proxies = {} # 定义一个字典用来存代理IP
        for i in range(len(proxies_list)): # 遍历每个IP
            proxies[str(i)] = proxies_list[i] # 记录每个IP
        return proxies
        
    def GetProxyInfo(): # 获取全部代理信息，期末大作业专用
        print('正在获取89IP的信息')
        proxies_info_1 = ProxyPool.ProxyPool_89ip.GetProxy_89ip_Info()
        print('正在获取IP3366的信息')
        proxies_info_2 = ProxyPool.ProxyPool_ip3366.GetProxy_ip3366_Info()
        print('正在获取快代理的信息(此过程较为缓慢)')
        proxies_info_3 = ProxyPool.ProxyPool_kuaidaili.GetProxy_kuaidaili_Info()
        
        proxies_info = proxies_info_1 + proxies_info_2 + proxies_info_3

        return proxies_info


# 主界面
def main():
    global states # 设置网站状态states为全局变量
    global mian # 设置程序初始化状态mian为全局变量
    os.system('cls') # 向终端发送命令:cls，清屏
    print('=====================================================')
    print('         代理IP获取          作者：碧霄-凝落@Ninglog')
    print('    项目地址:https://github.com/BX-NL/ProxyPool')
    print('=====================================================')
    if mian == '未初始化': # 检测程序是否第一次启动
        print(' 代理池初始化中。。。')
        time_used = ProxyPool.TestProxyPool() # 测试代理网站状态
        print(' 初始化完成!用时:', time_used)
        print('=====================================================')
        mian = '已初始化'
    else:
        pass
    print(' 1. ', states[0], '仅HTTP     ', urls['1'])
    print(' 2. ', states[1], '少量HTTPS  ', urls['2'])
    print(' 3. ', states[2], '匿名度高   ', urls['3'])
    print(' 0. ', '退出')
    print('=====================================================')
    select = str(input(' 请选择代理池：'))
    print('=====================================================')
    if select in ['1', '2', '3']:
        if states[int(select)-1] == '失败':
            print('=====================================================')
            print('服务器或网络异常')
            input('按Enter继续')
            mian = '未初始化'
        else:
            proxies = Proxy.GetProxy(select) # 获取代理IP
            os.system('cls')
            print('=====================================================')
            proxies = Proxy.TestProxy(proxies) # 改成TestProxy_True可以看到真实的测试结果
            print('=====================================================')
            input('按Enter键继续')
    elif select == '0': # 没想到吧，这个退出选项实际上是个重启选项
        print(' 退出失败!')
        mian = '未初始化'
    else: # 测试用端口
        pass


# 给其它程序留的接口,可获取一个或多个可用的代理IP
def proxies(num=1, sel=0): # 默认数量为1，sel默认为0(随机选择代理网站)
    proxies_full = {} # 这行删掉会报错，我也不知道为什么
    if sel == 0:
        key = random.sample(['1', '2', '3'], 1) # 随机选择一个代理网站
        proxies_full = Proxy.GetProxy(key[0]) # 从随机网站中获取一批代理IP
    else:
        proxies_full = Proxy.GetProxy(str(sel)) # 从指定的网站中获取一批代理IP

    proxies = {} # 定义一个字典用来保存代理IP
    key = random.sample(range(0, len(proxies_full) + 1), num) # 随机取一个或多个数
    if num == 1: # 随机挑选一个幸运IP
        agreement = re.match('https|http', proxies_full[str(key[0])]).group()  # 获取代理IP的协议
        agreement = agreement.upper() # 将协议转为大写，作为键值
        proxies[agreement] = proxies_full[str(key[0])] # 记录代理IP
    else:
        for i in range(num): # 遍历所有IP
            proxies[str(i)] = proxies_full[str(key[i])] # 记录代理IP

    return proxies


if __name__ == '__main__': # 只有运行本文件时才执行
    while True: # 不想做退出选项的原因
        main() # 显示界面
