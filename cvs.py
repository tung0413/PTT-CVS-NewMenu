import urllib.request as req
import bs4
import time
import datetime

mon = {'1': 'Jan', '2': 'Feb', '3': 'Mar', '4': 'Apr', '5': 'May', '6': 'Jun', '7': 'Jul', '8': 'Aug', '9': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}

def shop(str, month, date):
    str=str.strip('[商品] ')
    if str[0]=='7':
        tmpStr="7.11-"+mon[date]+".txt"
        #print (tmpStr)
        with open(tmpStr, mode="a", encoding="utf-8") as file:
            file.write(str[5:]+' '+month+"\n")
    elif str[0]=='全':
        tmpStr="FamilyMart-"+mon[date]+".txt"
        with open(tmpStr, mode="a", encoding="utf-8") as file:
            file.write(str[3:]+' '+month+"\n")
    elif str[0]=='萊':
        tmpStr="Hi-Life-"+mon[date]+".txt"
        with open(tmpStr, mode="a", encoding="utf-8") as file:
            file.write(str[4:]+' '+month+"\n")
    
def getData(url):
    request=req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    #print(data)

    root=bs4.BeautifulSoup(data, "html.parser")
    #print(root.title.string)

    date = time.strftime("%m").lstrip('0')

    divs=root.find_all("div", "r-ent")
    for d in divs:
        if d.find('a'):
            str=d.find('a').string
            if str[1]=="商":
                #print(d.find('div', 'date').string[:-3])
                if d.find('div', 'date').string.lstrip(' ')[:-3] == date:
                    #print(str+date)
                    month=d.find('div', 'date').string
                    shop(str, month, date)

    nextLink=root.find("a", string="‹ 上頁")
    return nextLink["href"]

pageUrl="https://www.ptt.cc/bbs/CVS/index.html"

count=0
while count<27:
    pageUrl="https://www.ptt.cc"+getData(pageUrl)
    count+=1
