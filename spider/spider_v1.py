# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 21:32:57 2017

@author: sj
"""

import os
import re
import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('Error0:Connect Failed!')
        
        
def get_city_rank():
#get popular city name and its rank in Euroup, and save to city_rank.txt
#version:0.1 (只获取了静态网页内容，还需改进，获取动态加载的更多城市信息)
    Europe_url = 'https://www.tripadvisor.cn/Tourism-g4-Europe-Vacations.html' 
    city_rank_html = get_html(Europe_url)
    
    city_soup = BeautifulSoup(city_rank_html,'html.parser')
    city_list = city_soup.find_all('a',{'class':'popularCity hoverHighlight'})
    
    city_fr = open('result_data/city_rank.txt','w')
    #wline = u'city_name,city_rank,city_url\n'
    #city_fr.write(wline)
    start_url = 'https://www.tripadvisor.cn'
    pat = re.compile(r'[0-9]+')
    for city in city_list:
        city_url = start_url+city['href']
        city_name = city.find('span',{'class':'name'}).get_text()
        city_rank = city.find('span',{'class':'rankNum'}).get_text()
        city_rank = pat.findall(city_rank)[0]
        wline = city_name+','+city_rank+','+city_url+'\n'
        city_fr.write(wline)
    city_fr.close()
    
def get_city_spot():
#for each city in city_rank.txt , get popular spots name,rank,url in the city, and save to a txt file named by city
#version:0.1 (只获取了静态网页内容，即每个城市景点排名中的第一页，还需改进，获取翻页之后的更多景点信息)    
    start_url = 'https://www.tripadvisor.cn'
    city_fr = open('result_data/city_rank.txt','r')
    for line in city_fr.readlines():
        eles = line.strip().split(',')
        city_url = eles[2]
        city_html = get_html(city_url)
        city_soup = BeautifulSoup(city_html,'html.parser')
        
        ##!!!下面获取城市中景点，缺乏通用性，因为这里有两种网页结构（也可能更多，目前发现两个），还不能通用，需要改进
       
        city_spot_url = city_soup.find_all('a',{'class':'seeAllLink'})[1]['href']
        city_spot_url = start_url + city_spot_url
        city_spot_html = get_html(city_spot_url)
        city_spot_soup = BeautifulSoup(city_spot_html,'html.parser')
        city_spot_list = city_spot_soup.find_all('div',{'class':'listing_title '})
        fr_name = 'result_data/city_spot/'+eles[1]+'_'+eles[0]+'.txt'
        spot_rank = 0
        with open(fr_name,'w') as city_spot_fr:
            for spot in city_spot_list:
                spot_rank = spot_rank+1
                spot_name = spot.get_text().strip()
                spot_url = spot.a['href']
                spot_url = start_url + spot_url
                wline = str(spot_rank)+','+spot_name+','+spot_url+'\n'
                city_spot_fr.write(wline)
        city_spot_fr.close()
        city_fr.close()
 
def get_spot_info(spot_url):  #未完待改
#for each spot , get its detail info
    spot_info_html = get_html(spot_url) 
    spot_soup = BeautifulSoup(spot_info_html,'html.parser')
    score = spot_soup.find_all('span',{'class':'overallRating'})[0].get_text()
    bussiness_time = spot_soup.find_all('div',{'class':'allHoursContainer'})[0].get_text()
    suggest_time = spot_soup.find_all('div',{'class':'detail_section duration'})[0].get_text()
    location = spot_soup.find_all('div',{'class':'detail_section address'})[0].get_text()
    contact = spot_soup.find_all('div',{'class':'detail_section phone'})[0].get_text()
    

get_city_rank()

get_city_spot()
       
path = 'result_data/city_spot'
files = os.listdir(path)
for file in files:   
     if not (os.path.isdir(file) or os.path.isdir(path + '/' + file)):
         city_fr = open(path+"/"+file,'r')
         for line in city_fr.readlines():
             eles = line.strip().split(',')
             spot_url = eles[2]
             get_spot_info(spot_url)  
         city_fr.close()
