import requests
import xmltodict
import json
import os
import os.path

basedir=os.path.join(cwd,'crawl','l1')
if not os.path.exists(basedir):
    print('creating', basedir)
    os.makedirs(basedir)

def get_url(url):
    headers={'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    return requests.get(url,headers=headers)

result=get_url('https://www.bizbuysell.com/sitemap_index.xml')
data=xmltodict.parse(result.text)

links_1=[ x['loc'] for x in data['sitemapindex']['sitemap']]

links_2=[]
for url in links_1:
    result=get_url(url)
    data=xmltodict.parse(result.text)
    #print(data)
    links_2.extend([ x['loc'] for x in data['urlset']['url']])

with open(ops.path.join(basedir,'links.json'),'w') as fh:
    json.dump((links_1,links_2),fh)
