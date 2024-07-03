## This code no longer works as of fall 2020. Ebay deprecated the finding library of their sdk.
from bs4 import BeautifulSoup
import csv
import datetime
import time
import requests
import urllib
import smtplib
import ssl
import os.path

today = "2020-04-25"

def prelim():
    from ebaysdk.finding import Connection as finding
    starttime = time.time()
    
    startdatetime = datetime.datetime.now()
    
    api = finding(appid= 'xxx', config_file=None, https=True)
    mykeywords = 'Prelim'
    mycatid = '6001'
    
    with open('D:/' +today+mykeywords+ '.csv', 'w' ,newline='',encoding='utf-8') as fp:
    
        for e in range(0,80):
            mykeywords = 1920+e
            mycatid = '6001'
            Dictionary_ApiRequest = {
                'keywords': mykeywords,
                'categoryId':mycatid,
                'paginationInput': {'pageNumber': '1'},
                'sortOrder':'EndTimeSoonest',
                'itemFilter': [
                        {'name': 'Condition', 'value': 'Used'},
                        {'name': 'LocatedIn', 'value': 'US'},
                        {'name': 'SoldItemsOnly', 'value': False}]}
            
            response = api.execute('findCompletedItems',  Dictionary_ApiRequest)
            soup = BeautifulSoup(response.content, 'lxml')
            
            totalentries = soup.totalentries.text
            totalpages = soup.totalpages.text
            totalpages2 = int(totalpages)
            totalentries2 = int(totalentries)   
            for x in range(1,totalpages2):
                
                Dictionary_ApiRequest = {
                    'keywords': mykeywords,
                    'categoryId':mycatid,
                    'paginationInput': {'pageNumber': x},
                    'sortOrder':'EndTimeSoonest',
                    'itemFilter': [
                            {'name': 'Condition', 'value': 'Used'},
                            {'name': 'LocatedIn', 'value': 'US'},
                            {'name': 'SoldItemsOnly', 'value': False}]}
                
                response = api.execute('findCompletedItems', Dictionary_ApiRequest)
                soup = BeautifulSoup(response.content, 'lxml')
            
                title = soup.findAll('title')
                price = soup.findAll('currentprice')
                start = soup.findAll('starttime')
                end = soup.findAll('endtime')
                location = soup.findAll('postalcode')
                status = soup.findAll('sellingstate')
                itemid = soup.findAll('itemid')
                listingtype = soup.findAll('listingtype')
                bestoffer = soup.findAll('bestofferenabled')
                buyitnow = soup.findAll('buyitnowavailable')
                watchcount = soup.findAll('watchcount')
                
                for i in range(len(title)):
                    if end[i].text[:10] != today:
                        next
                    else:
                        try:
                            listtocsv = [itemid[i].text,title[i].text,price[i].text,start[i].text,end[i].text,location[i].text,status[i].text,watchcount[i].text,listingtype[i].text,buyitnow[i].text,bestoffer[i].text]
                        except IndexError:
                            continue
                        b = csv.writer(fp,delimiter=',')
                        b.writerow(listtocsv)
    
    endtime = datetime.datetime.now()                  
    endtimesecs = ("--- %s seconds ---" % (time.time() - starttime))
    searchtimes = [startdatetime,endtime,endtimesecs]
    
    with open('D:/'+today+'PrelimSearchTimes.csv', 'w' ,newline='',encoding='utf-8') as fs:
        b = csv.writer(fs,delimiter=',')
        b.writerow(searchtimes)

def final():
    starttime = time.time()
    startdatetime = datetime.datetime.now()
    from ebaysdk.shopping import Connection as shopping
    api = shopping(appid= 'xxx', config_file=None, https=True)
    
    with open('D:/'+today+'Prelim.csv', 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        with open('D:/'+today+'Final.csv', 'w' ,newline='',encoding='utf-8') as fp:
            for line in csv_file:
                column = [line.split(',')[0]]
                itemid = str(column[0])
                dictitem = {'ItemID':itemid, 'IncludeSelector':'ItemSpecifics, TextDescription, Details'}
                try:
                    singleitem = api.execute('GetSingleItem', dictitem)
                except:
                    continue
                    print("Failed GetSingleItem call on "+itemid)
                    requests.get(api.execute('GetSingleItem', dictitem))
                    
                soup = BeautifulSoup(singleitem.content, 'lxml')
                itemid = soup.findAll('itemid')
                end = soup.findAll('endtime')
                start = soup.findAll('starttime')
                location = soup.findAll('postalcode')
                pictureurl = soup.find('pictureurl')
                postalcode = soup.findAll('postalcode')
                userid = soup.findAll('userid')
                feedbackscore = soup.findAll('feedbackscore')
                feedbackpercent = soup.findAll('positivefeedbackpercent')
                bidcount = soup.findAll('bidcount')
                price = soup.findAll('currentprice')
                listingstatus = soup.findAll('listingstatus')
                title = soup.findAll('title')
                hitcount = soup.findAll('hitcount')
                specifics = soup.findAll('name')
                conditiondesc = soup.findAll('conditiondescription')
                description = soup.findAll('description')
                
                try:
                    conditiondesc = conditiondesc[0].text
                except:
                    conditiondesc = 'null'
                
                try:
                    description = description[0].text
                except:
                    description = 'null'
                
                try:
                    pictureurl = pictureurl.text
                except:
                    pictureurl = 'null'
                
                sibs = [nm.findNextSibling() for nm in specifics]
                names = [nm.text for nm in specifics]
                values = [val.text for val in sibs]
                mydict = {k: v for k, v in zip(names, values)}
                
                try:
                    year = (mydict['Year'])
                except KeyError as error:
                    year = 'null'
                try:
                    make = (mydict['Make'])
                except KeyError as error:
                    make = 'null'
                try:
                    model = (mydict['Model'])
                except KeyError as error:
                    model = 'null'
                try:
                    trim = (mydict['Trim'])
                except KeyError as error:
                    trim = 'null'
                try:
                    mileage = (mydict['Mileage'])
                except KeyError as error:
                    mileage = 'null'
                try:
                    engine = (mydict['Engine'])
                except KeyError as error:
                    engine = 'null'
                try:
                    exteriorcolor = (mydict['Exterior Color'])
                except KeyError as error:
                    exteriorcolor = 'null'
                try:
                    manuexteriorcolor = (mydict['Manufacturer Exterior Color'])
                except KeyError as error:
                    manuexteriorcolor = 'null'
                try:
                    manuinteriorcolor = (mydict['Manufacturer Interior Color'])
                except KeyError as error:
                    manuinteriorcolor = 'null'
                try:
                    interiorcolor = (mydict['Interior Color'])
                except KeyError as error:
                    interiorcolor = 'null'
                try:
                    transmission = (mydict['Transmission'])
                except KeyError as error:
                    transmission = 'null'
                try:
                    legaltitle = (mydict['Vehicle Title'])
                except KeyError as error:
                    legaltitle = 'null'
                try:
                    forsaleby = (mydict['For Sale By'])
                except KeyError as error:
                    forsaleby = 'null'
                try:
                    subtitle = (mydict['SubTitle'])
                except KeyError as error:
                    subtitle = 'null'
                try:
                    vin = (mydict['VIN'])
                except KeyError as error:
                    vin = 'null'
                try:
                    listtocsv = (itemid[0].text, end[0].text, start[0].text, postalcode[0].text, userid[0].text, feedbackscore[0].text, feedbackpercent[0].text, bidcount[0].text, hitcount[0].text, listingstatus[0].text, title[0].text, price[0].text, year, make, model, trim, mileage, engine, exteriorcolor, manuexteriorcolor, interiorcolor, manuinteriorcolor, transmission, legaltitle, forsaleby, subtitle, conditiondesc, description, pictureurl)
                except:
                    continue
                b = csv.writer(fp,delimiter=',')
                b.writerow(listtocsv)
            
    endtime = datetime.datetime.now()                  
    endtimesecs = ("--- %s seconds ---" % (time.time() - starttime))
    searchtimes = [startdatetime,endtime,endtimesecs]
    
    with open('D:/'+today+'FinalSearchTimes.csv', 'w' ,newline='',encoding='utf-8') as fs:
        b = csv.writer(fs,delimiter=',')
        b.writerow(searchtimes)


def pictures():
    
    starttime = time.time()
    startdatetime = datetime.datetime.now()
    
    with open('D:/'+today+'Final.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            itemidtitle = row[0]
    
            pictureurl = row[28]
            pictureurlfixed = pictureurl[:59]+'$_4.JPG?set_id=880000500F'
    
            try:
                urllib.request.urlretrieve(pictureurlfixed,'D:/'+itemidtitle+'.jpg')
            except:
                next
                
    endtime = datetime.datetime.now()                  
    endtimesecs = ("--- %s seconds ---" % (time.time() - starttime))
    searchtimes = [startdatetime,endtime,endtimesecs]
    
    with open('D:/'+today+'PictureSearchTimes.csv', 'w' ,newline='',encoding='utf-8') as fs:
        b = csv.writer(fs,delimiter=',')
        b.writerow(searchtimes)

def email():
    prelimfile = ('D:/'+today+'Prelim.csv')
    finalfile = ('D:/'+today+'Final.csv')
    
    if os.path.exists(prelimfile):
        prelim = 'COMPLETED'
        #prelimrows = sum(1 for row in open(prelimfile))
    else:
        prelim = 'FAILED'
        #prelimrows = '0'
        
    if os.path.exists(finalfile):
        final = 'COMPLETED'
        #finalrows = sum(1 for row in open(finalfile))
    else:
        final = 'FAILED'
        #finalrows = '0'
    
    #messagetext = ' preliminary search ' + prelim + ' ('+prelimrows+' rows) and final search '+final +' ('+finalrows+' rows)'
    messagetext = ' preliminary search ' + prelim + ' and final search '+final
    
    port = 465  # For SSL
    smtp_server = "xxx"
    sender_email = "xxx"  # Enter your address
    receiver_email = "xxx"  # Enter receiver address
    password = 'xxx'
    message = '\
    Subject: Today '+ today + messagetext
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

prelim()
final()
pictures()
#email()
print("completed "+today)
