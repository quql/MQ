# -*- coding: utf-8 -*-
import requests
url='https://www.qqlong.top/sendceshi'
datas={'num':'1','key':'qql'}
def post(url, datas):
    response = requests.post(url,data=datas)
    json = response.json()
    print json
post(url,datas)