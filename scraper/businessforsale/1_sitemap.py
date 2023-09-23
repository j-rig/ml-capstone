import requests
import xmltodict
import json
import os
import os.path
import sys

def get_url(url):
    headers={'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    return requests.get(url,headers=headers)

result=get_url('https://us.businessesforsale.com/sitemap')
# print(result.text)
data=xmltodict.parse(result.text)
# print(data)

links_1=[ x['loc'] for x in data['sitemapindex']['sitemap']]

links_2=[]
i=0
for url in links_1:
    result=get_url(url)
    data=xmltodict.parse(result.text)
    print(i)
    #sys.exit(0)
    if 'url' in data['urlset'].keys():
        #print(data)
        urls=list(data['urlset']['url'])
        #print(type(urls))
        if type(urls[0]) is dict:
            # print(urls)
            # print(type(urls[0]))
            links_2.extend([ x['loc'] for x in urls])
        elif type(urls) is dict:
            links_2.append(urls['loc'])
        # if type(data['urlset']['url']) is list():
        #     links_2.extend([ x['loc'] for x in data['urlset']['url']])
        # else:
        #     print(data['urlset']['url'])
        #     links_2.append(data['urlset']['url']['loc'])
    i+=1

cwd=os.getcwd()

basedir=os.path.join(cwd,'crawl','l1')
if not os.path.exists(basedir):
    print('creating', basedir)
    os.makedirs(basedir)

linkspath=os.path.join(basedir,'links.l1.json')
with open(linkspath,'w') as fh:
    json.dump((links_1,links_2),fh)
