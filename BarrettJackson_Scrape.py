from bs4 import BeautifulSoup
import requests
import csv

url = 'https://www.barrett-jackson.com/Archive/Event/Docket/Scottsdale-2014/Collector-Cars/a5e00be7-6cc1-43ac-a77f-709b6556c5b8/01-14-2014/01-19-2014'

def get_page_links(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    print (r.status_code)
    print(r.headers)
    results = soup.findAll('div', class_="media searcher no-reserve ")
    links = [result.a['href'] for result in results]
    return links

def get_listing_data(url_end):
    url = "http://www.barrett-jackson.com"+url_end
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup
    
def make_car_dict(results):
    car_dict = {'Auction':'','Reserve':'','Status':'','Price':'','Year':'','Make':'','Model':'',
                'VIN':'','Exterior Color':'','Interior Color':'','Lot':'',}
    for category in car_dict:
        car_dict[category] = results.find('span', id=category).text

    b = csv.writer(fp,delimiter=',')
    b.writerow(car_dict.values())

def get_desc(results):
        descriptions = results.findAll('div', class_="hellcat-section-inner")
        print(descriptions[1].text)
        b = csv.writer(fp,delimiter=',')
        b.writerow(descriptions[1])
        
car_url_list = get_page_links(url)
print('links retrieved')
with open('file.csv', 'w' ,newline='') as fp:
    for i, link in enumerate(car_url_list):
        print('trying #', i, 'url'+link)
        limit = 2000
        if i == limit:
            break
        try:
            results = get_listing_data(link)
            make_car_dict(results)
            get_desc(results)

        except Exception:
            continue
