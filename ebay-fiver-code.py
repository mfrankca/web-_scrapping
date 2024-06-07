import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import time
import json

session=requests.Session()

rows=[]
def scrape(item):
    try:
        header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'en-US,en;q=0.9',
            'Sec-Ch-Ua-Mobile':'?0',
            'Sec-Ch-Ua-Model':'""',
            'Sec-Ch-Ua-Platform':'"Windows"',
            'Sec-Fetch-Dest':'document',
            'Sec-Fetch-Mode':'navigate',
            'Sec-Fetch-Site':'none',
            'Sec-Fetch-User':'?1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        url='https://www.ebay.com/itm/'+str(item).strip()
        # print(url)
        print('Scraping '+str(item).strip())
        r=session.get(url,headers=header, timeout=20)
        Soup=BeautifulSoup(r.content,'html.parser')
        row={}
        try:
            title = Soup.find('h1',attrs={'class':'x-item-title__mainTitle'}).text.replace('Details about','').strip()
        except:
            title = 'Not Available'
        try:
            price = Soup.find('div',attrs={'class':'x-price-primary'}).find('span').text.split('$')[-1].strip()
        except:
            price = 'Not Available'
        try:
            seller = Soup.find('div',attrs={'class':'ux-seller-section__item--seller'}).find('span',attrs={'class':'ux-textspans--BOLD'}).text.strip()
        except:
            seller = 'Not Available'

        try:
            qty=Soup.find('div',attrs={'class':'d-quantity__availability'}).find('span').text.replace('available','').replace('More than','').strip()
        except:
            qty='1'
        row['Title']=title
        row['Price']=price
        row['Quantity']=qty
        row['code']=url
        row['Seller']=seller
        img1 = ''
        img2 = ''
        img3 = ''
        try:
            # img1 = Soup.findAll('button',{'class':'image'})[0].find('img').get('src').replace('s-l64','s-l900')
            # img1 = Soup.find_all('img',{'class':'ux-image-magnify__image--original'})[0].get('data-onload-src')
            # img1 = Soup.find('div',{'class':'ux-image-carousel img-transition-medium'}).find_all('img')[0].get('data-onload-src')
            img1 = Soup.find('div',{'class':'ux-image-carousel-container'}).find_all('img')[0].get('data-zoom-src')
        except Exception as e:
            img1 = ''
        try:
            # img2 = Soup.findAll('button',{'class':'image'})[1].find('img').get('src').replace('s-l64','s-l900')
            # img2 = Soup.find_all('img',{'class':'ux-image-magnify__image--original'})[1].get('data-src')
            # img2 = Soup.find('div',{'class':'ux-image-carousel img-transition-medium'}).find_all('img')[1].get('data-src')
            img2 = Soup.find('div',{'class':'ux-image-carousel-container'}).find_all('img')[1].get('data-zoom-src')
        except:
            img2 = ''
        try:
            # img3 = Soup.findAll('button',{'class':'image'})[2].find('img').get('src').replace('s-l64','s-l900')
            # img3 = Soup.find_all('img',{'class':'ux-image-magnify__image--original'})[2].get('data-src')
            # img3 = Soup.find('div',{'class':'ux-image-carousel img-transition-medium'}).find_all('img')[2].get('data-src')
            img3 = Soup.find('div',{'class':'ux-image-carousel-container'}).find_all('img')[2].get('data-zoom-src')
        except:
            img3 = ''
        row['Image URL 1'] = img1
        row['Image URL 2'] = img2
        row['Image URL 3'] = img3
        table = Soup.find('div',attrs={'id':'viTabs_0_is'})
        labels = table.findAll('div', {'class': 'ux-labels-values__labels-content'})
        values = table.findAll('div', {'class': 'ux-labels-values__values-content'})
        for nth,label in enumerate(labels):
            row[label.getText()]=values[nth].getText()
        rows.append(row)
        # df=pd.DataFrame(rows)
        # df.to_excel('Ebay.xlsx',index=False)
    except:pass
    
            
with open('getItemNumberTest1.txt','r') as f:
    data=f.read()
    data=data.split('\n')
data = [i.strip() for i in data]
data = [i for i in data if i !='']
header = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'en-US,en;q=0.9',
    'Cache-Control':'max-age=0',
    'Sec-Ch-Ua-Mobile':'?0',
    'Sec-Ch-Ua-Model':"",
    'Sec-Ch-Ua-Platform':'"Windows"',
    'Sec-Fetch-Dest':'document',
    'Sec-Fetch-Mode':'navigate',
    'Sec-Fetch-Site':'none',
    'Sec-Fetch-User':'?1',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
}
# session.headers.update(header)
resp=session.get('https://www.ebay.com',headers=header)
for item in data:
    try:
        data=scrape(item)
    # break
    except Exception as e:
        _,_,line_tb=sys.exc_info()
        line_num=line_tb.tb_lineno
        print(e ,str(line_num))

df=pd.DataFrame(rows)
df.to_excel('Ebay.xlsx',index=False)

