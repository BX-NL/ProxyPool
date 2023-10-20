**这是一个可以从某些代理网站获取代理IP的爬虫**

**闲着没事干的时候写的，bug等我有空再修。虽然说不修也能用（划掉）**

**需要安装request和BeautifulSoup库**

**可以直接运行[ProxyPool.py](https://github.com/BX-NL/ProxyPool/blob/main/ProxyPool.py)获取当天刷新的全部IP。**

**也可以通过以下代码调用接口获取指定数量的可用IP**

    import ProxyPool
        
    #num为需要的IP数量，留空默认值为1

    #一般情况下1<=num<=10，不建议过大，容易出点奇奇怪怪的bug
        
    proxies = ProxyPool.Proxy(num=1)

    print(proxies)


**返回的proxies为字典形式**

proxies格式示例:

{'0': 'http://192.168.1.1:80',

 '1': 'http://192.168.1.2:8080',
 
 '2': 'https://192.168.1.3:80}
