from bs4 import BeautifulSoup
import extruct
import pprint
import os
import os.path
import json
import random

# ll=['crawl/l1/accounting-businesses-and-tax-practices-for-sale/index.html']
#
# l2=['crawl/l2/Business-Asset/140-000-asset-sale-food-truck-and-catering-business-wood-fired-pizza/2004337/index.html',
#     'crawl/l2/Business-Auction/absolute-auction-auto-repair-shop/27935052/index.html',
#     'crawl/l2/Business-Opportunity/a-1-italian-restaurant-and-bar/2066075/index.html',
#     'crawl/l2/Business-Real-Estate-For-Lease/2nd-generation-prime-restaurant-space-for-lease-in-downtown-los-gatos/1980249/index.html',
#     'crawl/l2/Business-Real-Estate-For-Sale/61-ridge-rd-middletown-ct-2-units/2035215/index.html',
#     'crawl/l2/Start-Up-Business/area-scouts-franchising-licensing-sports-athlete-development/2039470/index.html'
#     ]

base_url='https://us.businessesforsale.com'

def parse_list_view(html):
    data = extruct.extract(html, base_url=base_url)
    soup = BeautifulSoup(html,'lxml')
    spl={}
    bcl=[]
    for k in data['json-ld']:
        if k['@type']=='BreadcrumbList':
            for i in k['itemListElement']:
                bcl.append(i['item']['name'].strip())
    for k in data['json-ld']:
        if k['@type']=='SearchResultsPage':
            for i in k['about']:
                if i['item']['@type'] == 'Product':
                    l={}
                    l['s_breadcrumbs']=bcl
                    #TODO page title / other data
                    #l['group_props']=dict(data['opengraph'][0]['properties'])
                    l['s_id']=i['item']["productId"]
                    l['s_name']=i['item']['name']
                    l['s_desc']=i['item']['description']
                    l['s_url']=i['item']['url']
                    #if 'offers' in i['item'].keys():
                    l['s_price']=i['item']['offers']['price']
                    if 'availableAtOrFrom' in i['item']['offers'].keys() and i['item']['offers']['availableAtOrFrom'] !=None:
                        l['s_local']=i['item']['offers']['availableAtOrFrom']['address']['addressLocality']
                        l['s_region']=i['item']['offers']['availableAtOrFrom']['address']['addressRegion']
                    spl[l['s_id']]=l
            pl={}
            for c in ['diamond','showcase','basic']:
                for listing in soup.find_all(f'app-listing-{c}'):
                    l={}
                    l['id']=listing.find('a',{'class':c}).get('id')
                    l['href']=listing.find('a',{'class':c}).get('href')
                    l['title']=listing.find('h3',{'class':'title'}).text.strip()
                    loc=listing.find('p',{'class':'location'})
                    if loc is not None:
                        l['loc']=loc.text.strip()
                    l['desc']=listing.find('p',{'class':'description'}).text.strip()
                    cf=listing.find('p',{'class':'cash-flow'})
                    if cf is not None:
                        l['cash_flow']=listing.find('p',{'class':'cash-flow'}).text.strip()
                    ap=listing.find('p',{'class':'asking-price'})
                    if ap is not None:
                        l['asking_price']=ap.text.strip()
                    pl[l['id']]=l
    result=[]
    for k in spl.keys():
        z=spl[k].copy()
        if k in pl.keys():
            z.update(pl[k])
        result.append(z)
    return result

def parse_detail_view(html):
    data = extruct.extract(html, base_url=base_url)
    #return data
    pd={'s_breadcrumbs':[]}
    #todo parse LocalBusiness
    for k in data['json-ld']:
        if k['@type']=='BreadcrumbList':
            for i in k['itemListElement']:
                pd['s_breadcrumbs'].append(i['item']['name'].strip())
    for k in data['json-ld']:
        if k['@type']=='LocalBusiness':
            pd['s_b_desc']=k['description']
            pd['s_b_name']=k['name']
            pd['s_b_url']=k['url']
            pd['s_b_image']=k['image']
            if 'address' in k.keys() and k['address']['@type'] =='PostalAddress':
                if 'addressLocality' in k['address'].keys():
                    pd['s_b_local']=k['address']['addressLocality']
                if 'addressRegion' in k['address'].keys():
                    pd['s_b_region']=k['address']['addressRegion']
    for k in data['json-ld']:
        if k['@type']=='Product':
            if 'category' in k.keys():
                pd['s_category']=k['category']
            pd['s_desc']=k['description']
            pd['s_similar']=[]
            if 'isSimilarTo' in k.keys():
                for j in k['isSimilarTo']:
                    if 'productid' in j.keys():
                        pd['s_similar'].append(j['productid'])
            pd['s_name']=k['name']
            pd['s_id']=k['productid']
            pd['s_url']=k['url']
            if 'offers' in k.keys():
                pd['s_price']=k['offers']['price']
                if 'availableAtOrFrom' in k['offers']:
                    if 'addressLocality' in k['offers']['availableAtOrFrom']['address'].keys():
                        pd['s_local']=k['offers']['availableAtOrFrom']['address']['addressLocality']
                    if 'addressRegion' in k['offers']['availableAtOrFrom']['address'].keys():
                        pd['s_region']=k['offers']['availableAtOrFrom']['address']['addressRegion']

    soup = BeautifulSoup(html,'lxml')
    pd['p_title']=soup.find('title').text.strip()
    pc= soup.find('div',{'class':'pageContent'})
    if pc is None:
        ad=soup.find('app-bfs-auction-detail')
        if ad is not None:
            #print(ad)
            pd['auction']=True
            at=ad.find('h1')
            if at is not None:
                pd['p_auction_title']=ad.text.strip()
                pd['p_auction_location_text']=ad.find('div',{'id':'auction-location'}).text.strip()
                pd['p_auction_details_text']=ad.find('div',{'id':'auction-details'}).text.strip()
                pd['p_auction_highlights_text']=ad.find('div',{'id':'auction-highlights'}).text.strip()
                pd['p_auction_summary_text']=ad.find('div',{'id':'auction-executive-summary'}).text.strip()
                pf=ad.find('div',{'id':'auction-property-facts'})
                pd['p_auction_facts_text']=pf.text.strip()
                pfl=[]
                pfv=[]
                for k in pf.find_all('div',{'class':'property-fact-label'}):
                    pfl.append(k.text.strip())
                for k in pf.find_all('div',{'class':'property-fact-value'}):
                    pfv.append(k.text.strip())
                pd['p_auction_facts']=dict(zip(pfl,pfv))
                pd['p_auction_address_text']=ad.find('div',{'class':'auction-location-full-address'}).text.strip()
            #TODO get more info from auction page
        return pd
    pd['p_title']=pc.find('h1').text.strip()
    pd['p_location']=pc.find('h2').text.strip()
    fin=pc.find('div',{'class':'financials'})
    pd['p_financials_text']=fin.text.strip()
    pd['p_financials']={}
    for fi in fin.find_all('p'):
        k,v=fi.text.split(':')
        pd['p_financials'][k.strip()]=v.strip()
    bd=pc.find('div',{'class':'businessDescription'})
    pd['p_desc']=bd.text.strip()
    dt=pc.find('dl',{'class':'listingProfile_details'})
    if dt is not None:
        pd['p_details_text']=dt.text.strip()
        pdl=[]
        for di in dt.find_all(['dt','dd']):
            pdl.append(di.text.strip())
        pd['p_details']=pdl
    return pd

# for l in ll:
#     pprint.pprint(parse_list_view(open(l).read()))

# for l in l2:
#     pprint.pprint(parse_detail_view(open(l).read()))
#     #break

l1=[]
# for crawls in ("crawl/l1",):
#     for root, dirs, files in os.walk(crawls, topdown=False):
#         for name in files:
#             if name == 'index.html':
#                 dp=os.path.join(root,'data.json')
#                 hp=os.path.join(root,'index.html')
#                 l1.append((hp,dp))

random.shuffle(l1)
while(len(l1)):
    hp,dp=l1.pop()
    if not os.path.exists(dp):
        print('processing',hp)
        html=open(hp).read()
        data=parse_list_view(html)
        #pprint.pprint(data)
        json.dump(data,open(dp,'w'))
        #break
    else:
        print('skipping',hp)


l2=[]
for crawls in ("crawl/l2",):
    for root, dirs, files in os.walk(crawls, topdown=False):
        for name in files:
            if name == 'index.html':
                dp=os.path.join(root,'data.json')
                hp=os.path.join(root,'index.html')
                l2.append((hp,dp))

random.shuffle(l2)
while(len(l2)):
    hp,dp=l2.pop()
    if not os.path.exists(dp):
        print('processing',hp)
        html=open(hp).read()
        data=parse_detail_view(html)
        #pprint.pprint(data)
        json.dump(data,open(dp,'w'))
        #break
    else:
        print('skipping',hp)
