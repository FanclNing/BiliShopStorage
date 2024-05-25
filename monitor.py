import json
import time

import yaml

import LoadCk
import checkck

from Storage import Inquire

if __name__ == '__main__':
    t = time.localtime()
    print(f"当前时间：{t.tm_year}-{t.tm_mon}-{t.tm_mday}  {t.tm_hour}:{t.tm_min}:{t.tm_sec}")
    flag=False
    with open('api.yaml','r') as f:
        api=yaml.load(f,Loader=yaml.FullLoader)['api']
    with open('headers.yaml','r')as f:
        headers=yaml.load(f,Loader=yaml.FullLoader)
    with open('payload.yaml','r') as f:
        payload=yaml.load(f,Loader=yaml.FullLoader)

    while flag==False:
        flag=checkck.Check(api['my_info'],headers)
        if flag==False:
            headers['Cookie']=LoadCk.LoadCk()
            with open('headers.yaml','w') as f:
                yaml.dump(headers,f)


    a = Inquire()
    url = input("请输入查询商品的链接(支持长短链接)：")
    print(f'商品链接地址:{url}\n')
    a.SetUrl(url)
