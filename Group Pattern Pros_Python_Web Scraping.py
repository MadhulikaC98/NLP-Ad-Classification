#IMPORTING THE LIBRARIES
import requests
import random
import re
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
import schedule
import glob

#CREATING FAKE USER AGENTS
headers_list = [
    # Firefox 106 Win10
    {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 107.0 Win10
    {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 107.0 MacOS X
    {
    "Connection": "keep-alive",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Firefox 106 MacOS X
    {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.0; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
    }
]

#RANDOMIZING HEADERS
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers

#LIST OF CITIES AND LINKS
master_link = 'https://www.craigslist.org/about/sites#US'
master_html = r.get(master_link).text
soup2 = BeautifulSoup(master_html, 'html.parser')
us_cities = []
all_links = []
for li in soup2.find('h1').nextSibling.nextSibling.find_all('li'):
    try:
        all_links.append(li.find('a').get('href'))
    except:
        continue
    us_cities.append(li.text)


#GETTING THE LINKS FOR ALL SUBCATEGORIES WITHIN SALES
subcat_links = []
city = []
sub_cat = []
for ID, i in enumerate(all_links[:]):
    baseURL = i
    html = r.get(baseURL).text
    time.sleep(random.randint(0,3)+random.random())
    soup = BeautifulSoup(html, 'html.parser')
    truncated = soup.html.body.div.section.find('div', class_='housing').find('div', id='sss')
    for link in truncated.find_all('a')[1:]:
        subcat_links.append(baseURL+link.get('href'))
        sub_cat.append(link.find('span').contents[0])
        city.append(us_cities[ID])

#SAVING THE LINKS
fields = ['CITY', 'SUBCAT', 'LINK']
# data rows of csv file
rows = list(zip(city, sub_cat, subcat_links))

# name of csv file
filename = "subcategory_sales_links_all US CITIES.csv"

# writing to csv file
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
    # writing the fields
    csvwriter.writerow(fields)
    # writing the data rows
    csvwriter.writerows(rows)
csvfile.close()


#SCRAPING FOR 'GENERAL' POSTS (OR ANY 1 CATEGORY)
df = pd.read_csv('subcategory_sales_links_all US CITIES.csv')
df_general = df[df['SUBCAT']=='general']['LINK'] #CAN SCRAPE ANY CATEGORY
list_general = list(df_general)

headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers
sub_html = r.get(list_general[1]).text


headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers

#READING THE SUBLINK
pages = '#search=1~gallery~'
next = '~0'
no_of_links = len(list_general)
sublink_general = []
sub_category_general = []
post_links_general = []

for lin in range(no_of_links):
    sub_html = r.get(list_general[lin]).text
    soup_ref = BeautifulSoup(sub_html, 'html.parser')
    sublinks = []
    for sub in soup_ref.find_all('h3'):
        sublinks.append(sub.a.get('href'))
    sublinks_copy = sublinks.copy()
    number = 2
    soup3 = BeautifulSoup(sub_html+pages+str(number)+next, 'html.parser')
    sublinks_try = []
    for sub in soup3.find_all('h3'):
        sublinks_try.append(sub.a.get('href'))
    #TAKING
    while sublinks_copy!=sublinks_try:
        sublinks = sublinks + sublinks_try
        sublinks_try = []
        soup3 = BeautifulSoup(sub_html+pages+str(number)+next, 'html.parser')
        for subx in soup_ref.find_all('h3'):
            sublinks_try.append(subx.a.get('href'))
        number += 1
        if number>3:
            break
        else:
            continue
    length = len(sublinks)
    subcatx = list(np.repeat('general',length)) #CHANGE NAME TO THE CATEGORY BEING SCRAPED

    post_links_general += sublinks
    sub_category_general += subcatx

print(len(sub_category_general))
print(len(post_links_general))

post_titles = []
post_contents = []
post_attributes = []
post_subcat = []

#RANDOMIZING HEADERS
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers

#READING THE POST FROM THE LINK
for number, linky in enumerate(post_links_general[:1500]):
    headers = random.choice(headers_list)
    r = requests.Session()
    r.headers = headers
    post_html = r.get(linky).text
    soup_post = BeautifulSoup(post_html, 'html.parser')
    time.sleep(random.random()+random.randint(2,5))
    print(linky)
    title_page = ''
    body_page = ''
    all_tags_on_page = []
    try:
        title_page = soup_post.h1.find('span', id='titletextonly').text
        post_titles.append(title_page)
    except:
        break
    try:
        body_page = soup_post.find('section', id='postingbody').text.replace('\n','').replace('QR Code Link to This Post','')
        post_contents.append(body_page)

    except:
        body_page = 'None'
        post_contents.append(body_page)
    try:
        attributes = soup_post.find('p', class_='attrgroup').find_all('span')
        all_tags_on_page = [xi.text for xi in attributes]
        post_attributes.append(all_tags_on_page)
    except:
        all_tags_on_page = ['None']
        post_attributes.append(all_tags_on_page)

    post_subcat.append(sub_category_general[number])

#SAVING THE FILE
master_general = list(zip(sub_category_general,post_titles,post_contents, post_attributes))
master_pd = pd.DataFrame(master_general)
master_pd.rename(columns={0:'SubCategory', 1:'Title', 2:'Body', 3:'Tags'}, inplace=True)
master_pd.to_excel('General.xlsx', index=False, encoding='utf-8-sig')
pdf = pd.read_excel('General.xlsx')

#READING LINKS FROM A CITY

df = pd.read_csv('subcategory_sales_links_all US CITIES.csv')
trunc_df = df[df['CITY']=='indianapolis']
sample_link = list(trunc_df.iloc[:,2])
sample_city = list(trunc_df.iloc[:,0])
sample_subcat = list(trunc_df.iloc[:,1])


headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers

#READING THE SUBLINK
pages = '#search=1~gallery~'
next = '~0'
no_of_links_in_city = len(sample_link)
sublink_entire_city = []
city_name = []
sub_category = []

for lin in range(no_of_links_in_city):
    sub_html = r.get(sample_link[lin]).text
    soup_ref = BeautifulSoup(sub_html, 'html.parser')
    sublinks = []
    for sub in soup_ref.find_all('h3'):
        sublinks.append(sub.a.get('href'))
    sublinks_copy = sublinks.copy()
    number = 2
    soup3 = BeautifulSoup(sub_html+pages+str(number)+next, 'html.parser')
    sublinks_try = []
    for sub in soup3.find_all('h3'):
        sublinks_try.append(sub.a.get('href'))
    #TAKING
    while sublinks_copy!=sublinks_try:
        sublinks = sublinks + sublinks_try
        sublinks_try = []
        soup3 = BeautifulSoup(sub_html+pages+str(number)+next, 'html.parser')
        for subx in soup_ref.find_all('h3'):
            sublinks_try.append(subx.a.get('href'))
        number += 1
        if number>3:
            break
        else:
            continue
    length = len(sublinks)
    cityx = list(np.repeat(sample_city[lin],length))
    subcatx = list(np.repeat(sample_subcat[lin],length))

    sublink_entire_city += sublinks
    sub_category += subcatx
    city_name += cityx

#Checking
print(len(city_name))
print(len(sub_category))
print(len(sublink_entire_city))
set(sub_category)

#RANDOMIZING THE ORDER IN WHICH LINKS ARE READ
pd1 = pd.DataFrame(zip(city_name,sub_category,sublink_entire_city))
pd1 = pd1.sample(frac=1, random_state=0)
sublink_entire_cityX = list(pd1[2].copy())
sub_categoryX = list(pd1[1].copy())

post_titles = []
post_contents = []
post_attributes = []
post_subcat = []

#RANDOMIZING HEADERS
headers = random.choice(headers_list)
r = requests.Session()
r.headers = headers

#READING THE POST FROM THE LINK
for number, linky in enumerate(sublink_entire_cityX):
    headers = random.choice(headers_list)
    r = requests.Session()
    r.headers = headers
    post_html = r.get(linky).text
    soup_post = BeautifulSoup(post_html, 'html.parser')
    time.sleep(random.random()+random.randint(1,5))
    print(linky)
    # print(sub_categoryX[number])
    # print(BeautifulSoup.prettify(soup_post))
    title_page = ''
    body_page = ''
    all_tags_on_page = []
    try:
        title_page = soup_post.h1.find('span', id='titletextonly').text
        post_titles.append(title_page)
    except:
        title_page = 'None'
        post_titles.append(title_page)
    try:
        body_page = soup_post.find('section', id='postingbody').text.replace('\n','').replace('QR Code Link to This Post','')
        post_contents.append(body_page)

    except:
        body_page = 'None'
        post_contents.append(body_page)
    try:
        attributes = soup_post.find('p', class_='attrgroup').find_all('span')
        all_tags_on_page = [xi.text for xi in attributes]
        post_attributes.append(all_tags_on_page)
    except:
        all_tags_on_page = ['None']
        post_attributes.append(all_tags_on_page)

    post_subcat.append(sub_categoryX[number])

master = list(zip(post_subcat,post_titles,post_contents, post_attributes))
master_pd = pd.DataFrame(master)
master_pd.rename(columns={0:'SubCategory', 1:'Title', 2:'Body', 3:'Tags'}, inplace=True)
master_pd.to_excel('Indianapolis.xlsx', index=False, encoding='utf-8-sig')

#MERGING ALL OUTPUT FILES FROM SCRAPING TOGETHER
path = r'Final Scraped Data'
filenames = glob.glob(path + "\*.xlsx")
print('File names:', filenames)

excl_list = []
for file in filenames:
    df = pd.read_excel(file)
    df['City']= file[19:-5]
    excl_list.append(df)

excl_merged = pd.concat(excl_list, ignore_index=True)
excl_merged.drop_duplicates(inplace=True)
excl_merged.to_csv('Merged_excel_v2.csv')

