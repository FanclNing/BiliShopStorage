#在ck不存在或者过期的情况下获取ck
import json
import sys
import time

import requests
import urllib3
import yaml
import qrcode

from matplotlib import pyplot

urllib3.disable_warnings()
with open('api.yaml','r',encoding='utf-8') as f:
    api=yaml.load(f, Loader=yaml.FullLoader)['api']

with open('headers2.yaml', 'r')as f:
    headers=yaml.load(f, Loader=yaml.FullLoader)


def LoadCk():
    info=GetQrCode()
    print('登陆成功！')
    return info





def GetQrCode():
    try:
        data ={
            'source': 'main-fe-header'
        }

        res=requests.get(api['Get_Qrcode'],headers=headers,params=data,verify=False)
        res=json.loads(res.text)
        if res['code']==0:
            global qrurl,oauthKey
            qrurl=res['data']['url']
            oauthKey=res['data']['qrcode_key']
            print('请使用手机客户端扫描二维码登录')
            img=imgmaker(qrurl)
            ShowImage(img)
            info = CheckQrCode()
            CloseImage(img)
            return info
        else:
            print('获取二维码失败,尝试再次获取!')
            GetQrCode()
    except Exception as e:
        print(f'获取二维码失败!错误原因{e}')
        time.sleep(10)
        sys.exit()


def CloseImage(img):
    pyplot.close(img)
def ShowImage(img):
    pyplot.imshow(img)
    pyplot.axis('off')
    pyplot.show()
def imgmaker(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,  # 设置边框为0
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img
def CheckQrCode():
    try:
        input("扫完二维码之后按任意键继续...")
        data = {
            'qrcode_key': oauthKey,
            'source': 'main-fe-header'
        }
        res=requests.get(api['Check_QrLogin'],headers=headers,params=data,verify=False)
        data=json.loads(res.text)

        if data['data']['code'] ==0:
            info=Info(res.headers)
            return info
    except Exception as e:
        print(f"在检测是否扫码时发生未知错误，错误原因为{e}")
        time.sleep(10)
        sys.exit()

def Info(data):
    info=data['Set-Cookie']
    return info