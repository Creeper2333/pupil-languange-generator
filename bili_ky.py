import requests
from MyQR import myqr
from tkinter import *
from PIL import ImageTk,Image
import json,os
from bv2av import bv2av

def loginQr():
    print('打开b站客户端，扫码并确认后关闭扫码窗口即可。')
    headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host':'passport.bilibili.com'
    }
    rslt=requests.get('http://passport.bilibili.com/qrcode/getLoginUrl',
                  headers=headers,timeout=10)
    urlJson=json.loads('['+rslt.text+']')
    url=urlJson[0]['data']['url']
    sp=os.getcwd()+'\\'
    myqr.run(words=url,
         version=1,
         level='M',
         save_dir=sp,
        )
    root=Tk()
    root.resizable(width='false', height='false')
    root.title='QrCode'
    label=Label(root,text='使用b站客户端扫码，扫完关掉窗口')
    label.grid(row=0,column=0)
    img=Image.open('qrcode.png')
    photo=ImageTk.PhotoImage(img)
    imglabel=Label(root,image=photo)
    imglabel.grid(row=1,column=0,columnspan=3)
    root.mainloop()
    return urlJson

def loginRslt(data):
    headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host':'passport.bilibili.com'
    }
    postData={}
    postData.update(oauthKey=data[0]['data']['oauthKey'])
    #print(postData)
    loginInfo=requests.post('http://passport.bilibili.com/qrcode/getLoginInfo',
                           headers=headers,data=postData,timeout=10)
    #print(loginInfo.text)
    #print(str(loginInfo.cookies))
    return loginInfo

def bv_to_av(x):
    return bv2av(x)

def run_login():
    info=loginRslt(loginQr())
    sessdata=info.cookies['SESSDATA']
    bili_jct=info.cookies['bili_jct']
    return sessdata,bili_jct

def send_comment(csrf,sess,bvid,message,type='1'):
    headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host':'api.bilibili.com',
    'Content-Type':'application/x-www-form-urlencoded',
    'charset':'utf-8'
    }
    data={
        'csrf':csrf,
        'oid':str(bv_to_av(bvid)),
        'type':type,
        'message':message
    }
    c={
        'SESSDATA':sess
    }
    result=requests.post('http://api.bilibili.com/x/v2/reply/add',headers=headers,data=data,cookies=c,timeout=10)
    return result