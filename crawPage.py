__author__ = 'pc'
# -*- coding: utf-8 -*-
import sys
import urllib2
import requests
import re
import time
from xml.etree import ElementTree
from lxml import etree
from bs4 import BeautifulSoup
import lxml.html.soupparser as soupparser
import lxml.etree as etree

stdout = sys.stdout
reload (sys)

sys.stdout = stdout
sys.setdefaultencoding('utf8')

user='frank2236@sina.com'
pwd='unique'

proxies={'http':'61.183.128.2:4000','https':'61.183.128.2:4000'}
user_agent ='Mozilla/5.0 (Windows NT 6.2; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
headers1 = { 'User-Agent' : user_agent,'Referer' : 'https://www.linkedin.com/uas/login?goback=&trk=hb_signin'}
s=requests.session()

r = s.get('https://www.linkedin.com/',headers=headers1,proxies=proxies)
print '--------------',r.history
print 'r',r.status_code,

soup = BeautifulSoup(r.text)
loginCsrfParam = soup.find('input', id = 'loginCsrfParam-login')['value']
csrfToken = soup.find('input', id = 'csrfToken-login')['value']
sourceAlias = soup.find('input', id = 'sourceAlias-login')['value']
payload = { 'session_key': user, 'session_password': pwd, 'loginCsrfParam' : loginCsrfParam, 'csrfToken' : csrfToken, 'sourceAlias' : sourceAlias }
r=s.post('https://www.linkedin.com/uas/login-submit',headers=headers1, data=payload,proxies=proxies)

print r.history,'r',(len(r.history))
url='https://www.linkedin.com/profile/view?id=7924932&authType=name&authToken=BAU0&offset=1&trk=prof-sb-pdm-similar-photo'
url2='http://www.linkedin.com/profile/view?id=25029547&authType=OUT_OF_NETWORK&authToken=BT9-&locale=en_US&srchid=2297418701433309546941&srchindex=10&srchtotal=51527&trk=vsrp_people_res_name&trkInfo=VSRPsearchId%3A2297418701433309546941%2CVSRPtargetId%3A25029547%2CVSRPcmpt%3Aprimary%2CVSRPnm%3A'
url3='https://www.linkedin.com/profile/view?id=76101395&authType=name&authToken=mnQ9&trk=prof-sb-browse_map-name'
h1=s.get(url)
print h1.history,'111111111111111'
h=h1.text
sop=BeautifulSoup(h)
req = re.compile("<.*?>")
tree = etree.HTML(h)
count =1
f=open("G:/777.txt",'a')


f.write( '##Section %d ---BaseInfo:\n'%count)
exp=sop.find(attrs={'class':'full-name'})#name
f.write( 'NAME:  '+exp.text+'\n')
exp1=sop.find(attrs={'id':'headline'})#headline
f.write( 'Position:  '+exp1.text+'\n')
exp=sop.find(attrs={'class':'locality'})#local
f.write( 'Location:  '+exp.text+'\n')
exp2=sop.find(attrs={'class':'industry'})#industry
f.write( 'Industry:  '+exp2.text+'\n')

current=sop.find(attrs={'id':'overview-summary-current'})#current
nodes=current.td.ol

print 'Current: ',

f.write('Current: '+" ".join(str(node.text) for node in nodes)+'\n')
for node in nodes:
    print node.text,
print '\n'
past=sop.find(attrs={'id':'overview-summary-past'})#industry
nodes=past.td.ol

f.write('\nPrevious:  '+" ".join(str(node.text) for node in nodes)+'\n')
print 'Previous:  ',
for node in nodes:
    print node.text,
print '\n'
edu=sop.find(attrs={'id':'overview-summary-education'})#industry
f.write( '\nEducation:  '+edu.td.ol.li.text+'\n')


summary=sop.find(attrs={'class':'summary'})#summary
if summary is not None:
    count=count+1
    f.write('\n##Section %d ---Summary: \n'%count)
    f.write( summary.p.text+'\n')
#experience
try:
    exp=tree.xpath('//*[@id="background-experience"]/*')
    if exp :
        count=count+1
        f.write( '\n#Section %d ---%s \n'%(count,exp[0].text))
        ct=1
        for i in range(1,len(exp)-1):
            if exp[i].tag=='div' and  re.match('experience[-][0-9]*',exp[i].get('id')):
                node=exp[i][0]
                header=node[0]
                info1=re.sub(req,'',etree.tostring(header[1]))
                info2=re.sub(req,'',etree.tostring(header[2]))
                f.write( '\n#Experience%d: %s      '% (ct,info1)+' '+info2+'\n')
                #print '\n#Experience%d: %s      '% (ct,node[0][1][0].text),node[0][2][0][0][0].text


                ct=ct+1
                result=''
                for child in node[1]:
                    if child.tail is not None:
                         result+=child.text+' '+child.tail+'\n'
                    else:
                        result+= child.text+'\n'
                f.write(result+'\n')
                print '\n'
                string=etree.tostring(node[2])
                info=re.sub(req,'',string)
                f.write(info+'\n')
except Exception,ex:
    print Exception,ex



exp=sop.find(attrs={'id':'background-honors'})#hornors
if exp :
    count=count+1
    f.write('\n##Section %d ---%s\n'%(count,exp.h3.text))
    #print nodes
    cnt=1
    req = re.compile("<.*?>")
    try:

        for node in exp.children:
            if node.name=='div':
                nd=node.div.div
                span=nd.h5.find_next_siblings()
                f.write( '#Honor %d:'%cnt+' '+nd.h4.text+'\n')
                f.write( nd.h5.text+'\n')
                info = re.sub(req,'',str(span[0]))
                f.write( info+'\n')
                f.write( nd.p.text+'\n')
                cnt=cnt+1


    except Exception,ex:
        print Exception,ex

'''
exp=sop.find(attrs={'class':'skills-section'})#experien
print exp.contents
req=re.compile('<li data-endorsed-item-name="(.*?)"')
print str(exp)
nodes=re.findall(req,str(exp))
print nodes
'''

#skill

nodes=tree.xpath('//*[@id="profile-skills"]/*')
if nodes :
    count=count+1
    print '\n##Section %d ---Skill:\n'%(count,)
    for node in nodes:
        if(node.tag=='h5'):
            f.write( '#'+node.text+'\n')
        else:
            '''for child in node:
                skill=child.get('data-endorsed-item-name')
                if skill is not None:
                    print skill
            '''
            #f.write(','.join(node[i].get('data-endorsed-item-name') for i in range(len(node)))+'\n')
            result=''
            for i in range(0,len(node)-1):
                skill=node[i].get('data-endorsed-item-name')
                if skill is not None:
                    result+= skill+' '
            skill=node[-1].get('data-endorsed-item-name')
            if skill is not None:
                result+= skill+'\n'
            else:
                result+= '\n'
            f.write(result)


#education
try:
    edu=tree.xpath('//*[@id="background-education"]/*')
    if edu:
        count=count+1
        f.write('\n##Section %d ---%s:'%(count,edu[0].text)+'\n')
        for node in edu:
            if(node.tag=='div'):
                '''
                nd=BeautifulSoup(etree.tostring(node))
                child=nd.contents[0].contents[0]
                header=child.header
                span=header.find_next_siblings()
                info = re.sub(req,'',str(span[0]))
                print '#'+header[0].text
                print header[1].text
                for cd in header:
                    print cd.text
                '''
                nd=node[0][0]
                header=nd.find('header')
                info1=re.sub(req,'',etree.tostring(header[0]))
                info2=re.sub(req,'',etree.tostring(header[1]))
                f.write( '#'+info1+'\n')
                f.write(  info2+'\n')
                span=nd.find('span')
                
                result=''
                for child in span:
                    if child.tail is not None:
                        result+= child.text+' '+child.tail+' '
                    else:
                        result+= child.text+' '
                f.write(result+'\n\n')
                print '\n'
                p=nd.findall('p')
                #print dir (nd)
                result=''
                if p :
                    for np in p:
                        if np.get('class')=='activities':
                            for i in range(0,len(np)):
                                result+= np[i].text+' '
                            print '\n'
                            result+='\n'
                            f.write(result)
                        else:
                            f.write(np.text+'\n')

except Exception,ex:
    print '******'+Exception,ex

try:
    ad=tree.xpath('//*[@id="background-additional-info"]/*')
    if ad :
        build_text_list = etree.XPath("string()")
        count=count+1
        f.write('\n##Section %d ---%s:'%(count,ad[0].text)+'\n')
        for child in ad:
            if child.tag=='li':
                if child.get('id')=='interests' and len(child)>1:
                    f.write( '#'+child[0].text+'\n')
                    nd=child[1][0]
                    f.write(','.join(nd[i][0].text for i in range(len(nd)))+'\n')
                    for i in range(0,len(nd)-1):
                         print nd[i][0].text,',',
                    print nd[-1][0].text

                else:
                    if(len(child)>1):
                        f.write('\n#'+child[0].text+'\n')
                        print "#"+child[0].text
                        if child[1][0].text is not None :
                            f.write(child[1][0].text+'\n')
                        else:
                            string=re.sub(req,'',etree.tostring(child[1][0]))
                            if string is not None:
                                f.write( string +'\n')                           
                        

except Exception,ex:
    print 'info---------'+Exception,ex

f.close()




