from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import csv
import re

with open('file.csv', 'w' ,newline='') as fp:
    
    fname = "xxx"
    data = open(fname,'r')
    dataread = data.read()
    #print(dataread)
    soup = BeautifulSoup(dataread, 'lxml')
    prices = soup.findAll('span', class_='docketprice badge')
    name = soup.findAll('div', class_="media searcher no-reserve ")
    namereal = [result.a['name'] for result in name]
    #image = soup.findAll('img', class_="media-object lazy")
    iterationlength = len(namereal)
    pattern = re.compile("\*$")
    
    for i in range(iterationlength):
        try:
            if re.search(pattern,prices[i].text) != None:
                listtocsv = [namereal[i],prices[i].text]
                b = csv.writer(fp,delimiter=',')
                b.writerow(listtocsv)
            else:
                listtocsv = [namereal[i],'']
                b = csv.writer(fp,delimiter=',')
                b.writerow(listtocsv)
        except Exception:
            continue