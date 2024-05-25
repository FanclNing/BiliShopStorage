#进阶版适配多规格商品


import json
import os
import re
import sys
import time

import requests
import yaml
import urllib3
urllib3.disable_warnings()

class Inquire:
    def __init__(self):
        with open('api.yaml', 'r') as f:
            self.api = yaml.load(f, Loader=yaml.FullLoader)['api']
        with open('headers.yaml', 'r') as f:
            self.header = yaml.load(f, Loader=yaml.FullLoader)
        with open('payload.yaml', 'r') as f:
            self.payload = yaml.load(f, Loader=yaml.FullLoader)
        self.time=time.localtime()
        self.quit=True
        self.Storage="0"
        self.body={}
        self.name=""
        self.url=""
        self.itemsId=""
        self.skuId=""
        self.items=[]
        self.amount=""
        self.activityInfo={}
        self.specValues=""
        self.StorageAlert="---"
    def init(self):
        self.Storage = "0"
        self.body = {}
        self.skuId = ""
        self.items = []
        self.amount = ""
        self.activityInfo = {}
        self.specValues = ""
        self.StorageAlert = "---"

    #查询商品itemsId skuId activityinfos amount
    def GetInfo(self):
        url=self.api['GoodInfo']
        try:
            text=requests.get(url=self.url,headers=self.header).url
        except requests.exceptions.MissingSchema:
            print("             请查看链接是否正确！本次查询终止！")
            print("-------------------------END-------------------------")
            sys.exit()
        #获取商品istemsID
        self.itemsId=text.split("itemsId=")[1].split('&')[0].split('#')[0]


        payload={
             'itemsId':               self.itemsId
            ,'shopId':                ""
            ,'itemsVesion':           ""
            ,'v':                     self.GetWts()
        }

        res=requests.get(url=url,params=payload,headers=self.header)
        data=json.loads(res.text)
        itemsSkuList=data['data']['itemsSkuListVO']['itemsSkuList']
        self.name = data['data']['name']
        n=0
        for i in itemsSkuList:
            self.items=[]
            n+=1
            self.skuId=i['id']
            self.amount=i['price']
            self.specValues=i['specValues'][0]

            items={
                'cartId':'0'
                ,'itemsId':self.itemsId
                ,'skuId':self.skuId
                ,'skuNum':'1'
                ,'shopId':data['data']['shopId']
                ,'activityInfos':'null'
                ,'amount':self.amount
            }
            self.items.append(items)
            flag=1
            if data['data']['activityInfoVO']==None:
                activityId=0
                type=0
                flag=0
            else:
                activityId=data['data']['activityInfoVO']['activityId']
                type=data['data']['activityInfoVO']['type']

            activityInfo={
                'activityId':activityId
                ,'type':type
            }
            if flag!=1:
                activityInfo['marketingId']='null'
            self.body={
                'items':self.items
                ,'activityInfo':activityInfo
                ,"buyerId": '0'
                ,"distId": '0'
                ,"invoiceId": '0'
                ,"secKill": '0'
                ,"cartOrderType": '1'
                ,"cartTotalAmountAll": self.amount
                ,"freightCouponCodeId": ""
                ,"freightCouponIsChecked": 'false'
            }
            self.GetStorageInfo(n-1)
            self.PrintValues(res.text)
            print(f"--------------------No:{n}-END-------------------------")
        a=input("(输入f退出)请输入任意网址继续....")
        if a=="f":
            return None
        else:
            self.init()
            self.SetUrl(a)







    def PrintValues(self,res):
        data=json.loads(res)
        #输出部分优惠信息
        print(f"商品名称:{self.name}")
        print(f'商品规格:{self.specValues}')
        print(f"商品价格:{self.amount}")
        print(f'商品真实库存:{self.Storage},限购数量:{self.StorageAlert}')
        print(f"商品itemsId:{self.itemsId}")
        print(f"商品skuId:{self.skuId}")

        if data['data']['earlyBuyActivityInfo']==None:
            print("该商品没有早划算！")
        else:
            print("该商品有早划算!请记得准备!")
        if data['data']['europeanCompassActivityInfoVO'] ==None:
            print("该商品没有欧气宝箱！")
        else:
            print("该商品近期有欧气宝箱记得购买！")
        if data['data']['activityInfoVO']==None or data['data']['activityInfoVO']['activityId']!=6871048:
            print("该商品没有秒杀活动!")
        elif data['data']['activityInfoVO']['activityId']==6871048:
            print("该商品存在秒杀活动!")
        if data['data']['progressActivityInfoVO'] ==None:
            print("该商品没有满额权益！")
        else:
            print("该商品近期有满额权益，请及时购买！")
            print(data['data']['progressActivityInfoVO'][0]['description'])
        print()
        if not os.path.exists('history'):
            os.makedirs('history')
        with open(f'history\\{self.time.tm_year}-{self.time.tm_mon}-{self.time.tm_mday}查询历史.txt', 'a') as f:
            f.write('\n')
            f.write(f"\n{self.time.tm_hour}：{self.time.tm_min}查询状态\n")
            f.write(f"商品名称:{self.name}\n")
            f.write(f'商品规格:{self.specValues}\n')
            f.write(f"商品价格:{self.amount}\n")
            f.write(f'商品真实库存:{self.Storage}\n')



    def GetStorageInfo(self,n):
        try:
            url=self.api['Storage_Check']
            self.payload['v']=self.GetWts()
            res=requests.post(url=url,params=self.payload,headers=self.header,json=self.body)
            data = json.loads(res.text)
            if data["message"]!='success':
                print("登陆错误，请检查cookie是否正确！本次查询终止！")
                print("-------------------------END-------------------------")
                sys.exit()
            i = data['data']['orderList'][0]['itemsList'][0]
        except IndexError as e:
            print('商品正在预售中查询库存无意义，本次查询终止！')

            #预售商品解决方式
            #url='https://mall.bilibili.com/mall-c-search/items/info?'
            #self.payload['v'] = self.GetWts()
            #res = requests.post(url=url, params=self.payload, headers=self.header, json=self.body)
            #print("请查看链接是否正确！或者商品是否为现货(缺货）！本次查询终止！")
            #print("-------------------------END-------------------------")
            return None
        self.Storage=i['storage']
        if i['storageAlert']==0:
            i['storageAlert']=9999
        self.StorageAlert=i['storageAlert']



    def SetUrl(self,url):
        self.url=url
        print("正在爬取页面信息请稍后...")
        self.GetInfo()
    def GetWts(self):
        t = time.time()
        v = int(round(t * 1000))
        return v





if __name__ == '__main__':
    t=time.localtime()
    print(f"当前时间：{t.tm_year}-{t.tm_mon}-{t.tm_mday}  {t.tm_hour}:{t.tm_min}:{t.tm_sec}")
    a = Inquire()
    url=input("请输入查询商品的链接(支持长短链接)：")
    print(f'商品链接地址:{url}\n')
    a.SetUrl(url)


#测试链接 https://mall.bilibili.com/detail.html?loadingShow=1&noTitleBar=1&saleType=0&itemsId=10187297#noReffer=true&goFrom=na