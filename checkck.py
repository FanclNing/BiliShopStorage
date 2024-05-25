#旨在检测Ck是否过期
import json

import requests
import urllib3
urllib3.disable_warnings()

def Check(url,headers):
    res=requests.get(url=url,headers=headers,verify=False)
    data=json.loads(res.text)
    if data['code']==-500:
        print('ck失效')
        return False
    else:
        print('ck有效')
        return True


