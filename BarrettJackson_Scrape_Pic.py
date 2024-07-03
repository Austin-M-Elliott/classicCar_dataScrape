from bs4 import BeautifulSoup
import urllib
import csv
import requests

with open('file.csv', 'w' ,newline='') as fp:
    b = csv.writer(fp,delimiter=',')
    
    r = urllib.request.urlopen('http://www.barrett-jackson.com/Archive/Event/Docket/Northeast-2017/Collector-Cars/d03d8819-06f3-4278-9fdf-eab3acdd78a1/06-21-2017/06-24-2017').read()
    soup = BeautifulSoup(r, "lxml")
    results = soup.findAll('div', class_="media searcher no-reserve ")
            
    for x in range(0,7):
        first_result = results[x]
        
        href = first_result.a["href"]
        prefix = "http://www.barrett-jackson.com"
        
        newurl = urllib.parse.urljoin(prefix,href) #create new URL from prefix+href
        newsoup = urllib.request.urlopen(newurl) #create new soup with new URL
        soup2 = BeautifulSoup(newsoup, "lxml") #create new soup with new URL
        newresult = soup2.findAll('div', class_="span12 bj-section")
        auction = soup2.find('span', id="Auction").text
        reserve = soup2.find('span', id="Reserve").text
        status = soup2.find('span', id="Status").text
        price = soup2.find('span', id="Price").text
        year = soup2.find('span', id="Year").text
        make = soup2.find('span', id="Make").text
        model = soup2.find('span', id="Model").text
        VIN = soup2.find('span', id="VIN").text
        exterior_color = soup2.find('span', id="Exterior Color").text
        interior_color = soup2.find('span', id="Interior Color").text
        cylinders = soup2.find('span', id="Cylinders").text
        engine_size = soup2.find('span', id="Engine Size").text
        transmission = soup2.find('span', id="Transmission").text
        
        if auction == "N/A":
            auction = ""
        if reserve == "N/A":
            reserve = ""
        if status == "N/A":
            status = ""
        if price == "N/A":
            price = ""
        if year == "N/A":
            year = ""
        if make == "N/A":
            make = ""
        if model == "N/A":
            model = ""
        if VIN == "N/A":
            VIN = ""
        if exterior_color == "N/A":
            exterior_color = ""
        if interior_color == "N/A":
            interior_color = ""
        if cylinders == "N/A":
            cylinders = ""
        if engine_size == "N/A":
            engine_size = ""
        if transmission == "N/A":
            transmission = "" 
    
        data=[[newurl,auction,reserve,status,price,year,make,model,VIN,exterior_color,interior_color,cylinders,engine_size,transmission]]
        b.writerows(data)
        
        newresultpic = soup2.find('div', class_="car-thumb") #Picture
        pic_url = newresultpic.find('img')['src']
        image = requests.get(pic_url).content
        imagefilename = year+' '+make+' '+model+' '+VIN
        with open('/Users/Austin E/Documents/BarrettJackson/'+str(imagefilename)+'.jpg', 'wb') as handler:
            handler.write(image)
        
    