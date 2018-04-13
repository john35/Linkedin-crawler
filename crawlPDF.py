# -*- coding: utf-8 -*-
import urllib2
import re
import sys
import Queue
import threading
import time
import logging
import requests
from bs4 import BeautifulSoup
stdout = sys.stdout
reload (sys)

sys.stdout = stdout
sys.setdefaultencoding('utf8')

def get_session(header,user,pwd,proxies):
    try:
        s=requests.session()
        print 'gg'
        r = s.get('https://www.linkedin.com/',headers=header)
        print 'r',r.status_code
        print 'jj'
        soup = BeautifulSoup(r.text) 
        loginCsrfParam = soup.find('input', id = 'loginCsrfParam-login')['value'] 
        csrfToken = soup.find('input', id = 'csrfToken-login')['value'] 
        sourceAlias = soup.find('input', id = 'sourceAlias-login')['value']
        payload = { 'session_key': user, 'session_password': pwd, 'loginCsrfParam' : loginCsrfParam, 'csrfToken' : csrfToken, 'sourceAlias' : sourceAlias } 
        h=s.post('https://www.linkedin.com/uas/login-submit',headers=header, data=payload,proxies=proxies)
        
        print h.history
    except Exception,ex:
        print u'get_session 内异常发生:',Exception,":",ex
    return s
def get_pdf(que,s,header):
    global NUM
    try:
        
        string=que.get()
        namelist=string.split('lilianjie')
        print u'正在取队列中元素,队列元素个数：%d\n'%(que.qsize())
        t=s.get(namelist[1],headers=header)
        with open (namelist[0],"wb") as f:
            f.write(t.content)        
        
        lck.acquire()
        NUM=NUM+1
        print '第%d个pdf下载完成'%NUM,'\n'
        lck.release()
        time.sleep(2)
    except Exception,ex:
        print u'get_pdf 内异常发生:',Exception,":",ex
        time.sleep(3)
'''从主页中爬取每条的网址'''
def GetPage(que):
    global page
    string='https://www.linkedin.com/vsearch/p?keywords=ibm&orig=ADVS&pageKey=voltron_people_search_internal_jsp&rsid=2317490391432794404723&trkInfo=&search=Search&openFacets=N,G,CC&titleScope=CP&companyScope=CP&locationType=Y&countryCode=us&distance=50&page_num='
    
           
    req2=re.compile('https:[/][/]www\.linkedin\.com[/]profile[/]view[?]id=[0-9]{1,15}.*?2CVSRPnm[%]3A')
    req=re.compile(r'pdfFileName=(.*?)&')
    user='syangunique@hotmail.com'
    pwd='unique'
    proxies={'http':'61.183.128.2:4000','https':'61.183.128.2:4000'}       
    user_agent ='Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
    headers = { 'User-Agent' : user_agent }
    s=get_session(headers,user,pwd,proxies)
    print 'dd'
    count=0
    while True:
        if(page>100):
            time.sleep(1)
            get_text(que,s,headers)
            count=count+1
            print 'GetPage ciunt=',count
            if(count==5):
                count=0
                time.sleep(3)
                
            if(que.empty()):
                break
        else:
            dics={}
            if lp.acquire():    
                url =string+str(page)
                page=page+1
                print u'第%s页\n'%(page,)
            lp.release()
            try:
                h=s.get(url,headers=headers,proxies=proxies)
                h=h.text
                nodes = re.findall(req2,h)
                for node in nodes:
                    if 'trk=vsrp_people_res_name'in node:
                        hc=s.get(node,headers=headers,proxies=proxies)
                        hc=hc.text
                        sop=BeautifulSoup(hc)
                        tex=sop.find(attrs={'name':"exportToPdf"})['href']
                        pdfname=re.findall(req,tex)[0]
                        pdf_url='https://www.linkedin.com%s'%(tex)
                        filename='G:/pdf/ibm/%s'%(pdfname)+'.pdf'
                        node=filename+"lilianjie"+pdf_url
                        que.put(node)
                        time.sleep(1)
                print u'正在向队列input元素,队列元素个数：%d\n'%(que.qsize()),'page=',page
                time.sleep(2)
            except Exception,ex:
                print Exception,":",ex
                time.sleep(2)
            time.sleep(5)
        
        
    que.task_done()
        

def Save_PDF(que,header,user,pwd,proxies,i):
    global NUM
    s=get_session(header,user,pwd,proxies)
    count=1 
    while True:
        get_pdf(que,s,header)
        count=count+1
        if(count==3):
            count=0
            time.sleep(5)
        print 'Thread %d: count=%d'%(i,count)
        if(que.empty()):
            time.sleep(15)
    que.task_done()
    
        
try:
    
    user1='yourlinkedin_account name such as xxx@xxx.com'
    user2='xxx2@qq.com'
    user3='xxx3@163.com'

    pwd='yourlinkedin_password'

    proxies={'http':'61.183.128.2:4000','https':'61.183.128.2:4000'}
    user_agent3 ='Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
    user_agent2 ='Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)'
    user_agent1 ='Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2369.0 Safari/537.36'
    headers1 = { 'User-Agent' : user_agent1,'Referer' : 'https://www.linkedin.com/uas/login?goback=&trk=hb_signin'}
    headers2 = { 'User-Agent' : user_agent2,'Referer' : 'https://www.linkedin.com/uas/login?goback=&trk=hb_signin'}
    headers3 = { 'User-Agent' : user_agent3,'Referer' : 'https://www.linkedin.com/uas/login?goback=&trk=hb_signin'}
    user_list=[user1,user2,user3]
    headers_list=[headers1,headers2,headers3]                    
    que =Queue.Queue()
    threads=[]
    lck=threading.Lock()
    lp=threading.Lock()
    NUM=1
    print 'nihao'
    page=1
except Exception,ex:
    print u'try内异常发生:',Exception,":",ex
    
t =threading.Thread(target=GetPage,args=(que,))
t.setDaemon(True)
t.start()
time.sleep(30)
for i in range(1,3):
    
    r= threading.Thread(target=Save_PDF,args=(que,headers_list[i-1],user_list[i-1],pwd,proxies,i))
    r.setDaemon(True)
    time.sleep(2)
    r.start()
    
que.join()
    
