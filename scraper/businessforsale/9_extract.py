from bs4 import BeautifulSoup
import extruct
import pprint
import os
import os.path
import json
import random

# dl=['crawl/l1/us/2-furniture-stores-in-nassau-county-for-sale.aspx/index.html',
#     'crawl/l4/us/1-2m-cash-flow-two-highly-profitable-mitigation-and-construction-franchises-for-sale.aspx/index.html']
#
# ll=['crawl/l3/us/search/advertising-businesses-for-sale-5/index.html',
#     'crawl/l2/us/search/accountancy-practices-for-sale/index.html']


base_url='https://us.businessesforsale.com'


# def is_detail(soup):
#     pass
#
# def is_list(soup):
#     pass


def parse_detail_view(html):

    data = extruct.extract(html, base_url=base_url)
    # print('detail')
    #pprint.pprint(data)
    detail={}
    # for d in data['rdfa']:
    #     if d['@id'] == 'https://us.businessesforsale.com':
    #         detail['meta_url']=d['http://ogp.me/ns#url'][0]['@value']
    #         detail['meta_desc']=d['http://ogp.me/ns#description'][0]['@value']
    #         detail['meta_title']=d['http://ogp.me/ns#title'][0]['@value']
    detail['props']=dict(data['opengraph'][0]['properties'])
    soup = BeautifulSoup(html,'lxml')

    bd=soup.find('div',{'class':'broker-details-print'})
    if bd is not None:
        detail['broker_details']=bd.find('h4').text.strip()

    lid=soup.find('ul',{'class':'listing-id'})
    if lid is not None:
        detail['listing_id']=lid.find('span',{'id':'listing-id'}).text.strip()
        detail['listing_id_text']=lid.text.strip()

    lt=soup.find('div',{'class':'listing-title'})
    if lt is not None:
        detail['listing_title']=lt.find('h1').text.strip()
    else:
        print('not a listing...')
        return {}

    la=lt.find('div',{'id':'address'})
    #detail['address']=[a.text.strip() for a in la.find_all('span')]
    detail['address']=la.text.strip()

    lc=soup.find('div',{'id':'main-listing-content'})
    od=lc.find('div',{'class':'overview-details'})

    ap=od.find('dl',{'class':'price'})
    #detail['asking_price']=' '.join([s.text.strip() for s in ap.find_all('span')])
    detail['asking_price']=ap.find('dd').text.strip()

    rev=od.find('dl',{'id':'revenue'})
    detail['sales_revenue']=rev.find('dd').text.strip()

    pro=od.find('dl',{'id':'profit'})
    detail['cash_flow']=pro.find('dd').text.strip()

    listing=lc.find('div',{'class':'listing-section-content'})
    #detail['listing']=' '.join([p.text.strip() for p in listing.find_all('p')])
    detail['listing']=listing.text.strip()

    bisop=lc.find('div',{'id':'business-operation'})
    detail['business_operation']={}
    if bisop is not None:
        for i in bisop.find_all('dl'):
            k= i.find('dt').text.strip()
            v= i.find('dd').text.strip()
            detail['business_operation'][k]=v

    propi=lc.find('div',{'id':'property-information'})
    detail['property-information']={}
    if propi is not None:
        for i in propi.find_all('dl'):
            k= i.find('dt').text.strip()
            v= i.find('dd').text.strip()
            detail['property-information'][k]=v

    fterms=lc.find('div',{'id':'ranchise-terms'})
    detail['ranchise-terms']={}
    if fterms is not None:
        for i in fterms.find_all('dl'):
            k= i.find('dt').text.strip()
            v= i.find('dd').text.strip()
            detail['ranchise-terms'][k]=v

    oinfo=lc.find('div',{'id':'other-information'})
    detail['other_information']={}
    if oinfo is not None:
        for i in oinfo.find_all('dl'):
            k= i.find('dt').text.strip()
            v= i.find('dd').text.strip()
            detail['other_information'][k]=v

    return detail


def parse_list_view(html):
    data = extruct.extract(html, base_url=base_url)
    #pprint.pprint(data)
    og=dict(data['opengraph'][0]['properties'])
    soup = BeautifulSoup(html, 'lxml')

    con= soup.find('div', {'id': 'container'})

    tas=con.find('div', {'class': 'title-and-sort'})
    #print(tas)
    group_title=tas.find('h1').text.strip()
    # group_desc=tas.find('p').text.strip()

    result=[]
    sr= con.find('div', {'class': 'search-results'})
    for r in sr.find_all('div', {'class': 'result'}):
        rt=r.find('table', {'class': 'result-table'})
        detail=dict(group_title=group_title,group_props=og) #,group_desc=group_desc)
        detail['title']=rt.find('caption').text.strip()
        loc=rt.find('tr', {'class': 't-loc'})
        detail['location']=loc.find('td').text.strip()
        desc=rt.find('tr', {'class': 't-desc'})
        detail['description']=desc.find('p').text.strip()
        detail['url']=desc.find('a')['href']
        fin=rt.find('tr', {'class': 't-finance'})
        for rr in fin.find_all('tr'):
            k=rr.find('th').text.strip()
            v=rr.find('td').text.strip()
            detail[k]=v
        detail['tags']=[]
        tags=rt.find('tr', {'class': 't-tags'})
        for t in tags.find_all('li'):
            detail['tags'].append(t.text.strip())
        detail['labels']=[]
        lbl=rt.find('div', {'class': 'result-labels'})
        if lbl is not None:
            for l in lbl.find_all('span'):
                detail['labels'].append(l.text.strip())
        rc=r.find('div', {'class': 'result-contact'})
        sl=rc.find('div', {'class': 'save-listing'})
        if sl is not None:
            detail['save_url']=sl.find('a')['href']
        result.append(detail)

    return result

# for p in dl:
#     print('detail')
#     html=open(p).read()
#     r=parse_detail_view(html)
#     pprint.pprint(r)
#
#
# for p in ll:
#     print('list')
#     html=open(p).read()
#     r=parse_list_view(html)
#     pprint.pprint(r)

# def crawl_list_paths(wq):
#     for crawls in ("crawl/l2/us","crawl/l3/us"):
#         for root, dirs, files in os.walk(crawls, topdown=False):
#             for name in files:
#                 if name == 'index.html':
#                     wq.put(root)
#
# if __name__ == '__main__':
#     wq=Queue()
#     with Pool(5) as p:
#         p.apply(crawl_list_paths,[wq,])


l1=[]
for crawls in ("crawl/l2/us","crawl/l3/us"):
    for root, dirs, files in os.walk(crawls, topdown=False):
        for name in files:
            if name == 'index.html':
                dp=os.path.join(root,'data.json')
                hp=os.path.join(root,'index.html')
                l1.append((hp,dp))
                # if not os.path.exists(dp):
                #     print('processing',hp)
                #     # html=open(hp).read()
                #     # data=parse_list_view(html)
                #     # json.dump(data,open(dp,'w'))
                # else:
                #     print('skipping',hp)

l2=[]
for crawls in ("crawl/l1/us","crawl/l4/us"):
    for root, dirs, files in os.walk(crawls, topdown=False):
        for name in files:
            if name == 'index.html':
                dp=os.path.join(root,'data.json')
                hp=os.path.join(root,'index.html')
                l2.append((hp,dp))
                # if not os.path.exists(dp):
                #     print('processing',hp)
                #     # html=open(hp).read()
                #     # data=parse_detail_view(html)
                #     # json.dump(data,open(dp,'w'))
                # else:
                #     print('skipping',hp)

random.shuffle(l1)
while(len(l1)):
    hp,dp=l1.pop()
    if not os.path.exists(dp):
        print('processing',hp)
        html=open(hp).read()
        data=parse_list_view(html)
        json.dump(data,open(dp,'w'))
    else:
        print('skipping',hp)
random.shuffle(l2)
while(len(l2)):
    hp,dp=l2.pop()
    if not os.path.exists(dp):
        print('processing',hp)
        html=open(hp).read()
        data=parse_detail_view(html)
        json.dump(data,open(dp,'w'))
    else:
        print('skipping',hp)
