import ProxyPool

proxies = ProxyPool.ProxyAPI(num=1)

print(proxies)



proxies格式示例:
{'0': 'http://192.168.1.1:80'
 '1': 'http://192.168.1.2:8080'
 '2': 'https://192.168.1.3:80}