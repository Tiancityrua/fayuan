import requests
from bs4 import BeautifulSoup
import json
import time
import datetime
from config import *

def gethtml(url,data):
    response=requests.get(url,data)
    return response.text
#解析源码，找出每一个td的内容
def parsehtml(html):
    soup=BeautifulSoup(html,'lxml')
    table=soup.find("table",attrs={"id":"report"})
    trs=table.find("tr").find_next_siblings()
    #存放在一个list里面
    for tr in trs:
        tds=tr.find_all("td")
        yield [
            tds[0].text.strip(),
            tds[1].text.strip(),
            tds[2].text.strip(),
            tds[3].text.strip(),
            tds[4].text.strip(),
            tds[5].text.strip(),
            tds[6].text.strip(),
            tds[7].text.strip(),
            tds[8].text.strip(),
        ]
def writetofile(content):
    with open("re.txt",'a',encoding="utf-8") as f:
        f.write(json.dumps(content,ensure_ascii=False)+"\n")
#获得总页数
def getpagenums():
    baseurl="http://www.hshfy.sh.cn/shfy/gweb/ktgg_search_content.jsp?"
    datatime=datetime.date.fromtimestamp(time.time())
    data={
        "ktrqks": datatime,
        "ktrqjs": datatime,
    }
    while True:
        html=gethtml(baseurl,data)
        soup=BeautifulSoup(html,'lxml')
        break
    res=soup.find("div",attrs={"class":"meneame"})

    pagenums=res.find('strong').text

    pagenums=int(pagenums)
    if pagenums %15 ==0:
        pagenums=pagenums//15
    else:
        pagenums=pagenums//15+1
    print("总页数",pagenums)
    return pagenums

def main():
    pagenums=getpagenums()
    if not True:
        return
    baseurl="http://www.hshfy.sh.cn/shfy/gweb/ktgg_search_content.jsp?"
    while True:
        datatime=datetime.date.fromtimestamp(time.time())
        pagenum=1
        data={
            "ktrqks": datatime,
            "ktrqjs": datatime,
            "pagesnum": pagenum
        }
        #爬取每一页数据
        while pagenum<=pagenums:
            print(data)
            while True:
                html=gethtml(baseurl,data)
                soup=BeautifulSoup(html,'lxml')
                break
            res=parsehtml(html)
            for i in res:
                writetofile(i)
            print("爬取完第【%s】页,总共【%s】页" % (pagenum, pagenums))
            pagenum+=1
            data["pagesnum"]=pagenum
            time.sleep(1)
        else:
            print("wanbi")
        print("xiumian...")
        time.sleep(SLEEP_TIME)
if __name__=='__main__':
    main()