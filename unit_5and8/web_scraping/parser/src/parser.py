import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import time
import shutil
import xlwt

import requests
from bs4 import BeautifulSoup

#to get particular unit
def get_auto(suburl):
    sub_my_columns = ['bodyType', 'brand', 'color', 'fuelType',
                  'modelDate', 'name', 'numberOfDoors', 'productionDate',
                  'vehicleConfiguration', 'vehicleTransmission', 'engineDisplacement', 'enginePower',
                  'description', 'mileage', 'complectation', 'drive', 'hand', 'condition', 'owners',
                  'PTS', 'customs', 'owningTime', 'id' 'price']

    car = pd.Series(index = sub_my_columns)
    sub_r = requests.get(suburl, headers={'User-Agent': 'Mozilla/5.0'})
    sub_r.encoding = 'utf-8'
    soup = BeautifulSoup(sub_r.text, 'html.parser')

    target = soup.find('script', type='application/ld+json')
    try:
        l = target.contents[0].split(',')
        for el in l:
            pair = el.split('":')
            try:
                car[pair[0].replace('"','')] = pair[1].replace('"','')
            except:
                continue
    except:
        pass
                
    #The rest of the data we'll awkwardly parse from tech list by html tags  
    try:
        car['mileage'] = float(soup.find('li', class_="CardInfo__row CardInfo__row_kmAge").text.replace(
            'Пробег','').replace('км','').replace(u'\xa0', u''))
    except:
        car['mileage'] = 0.0
   
    try:
        sstr = soup.find('div', class_="ComplectationGroups")
        sstr = str(sstr.text)
        car['complectation'] = ''.join(';' + char if char.isupper() else char for char in sstr).strip()
    except:
        car['complectation'] = np.nan
        
    try:
        target = soup.find('li', class_="CardInfoRow CardInfoRow_wheel")
        car['hand'] = target.contents[1].text
    except:
        car['hand'] = 'левый'
    
    try:
        target = soup.find('li', class_="CardInfoRow CardInfoRow_drive")
        car['drive'] = target.contents[1].text
    except:
        car['drive'] = np.nan
        
    try:
        target = soup.find('li', class_="CardInfoRow CardInfoRow_state")
        car['condition']= target.contents[1].text
    except:
        car['condition'] = np.nan
        
    try:
        target = soup.find('li', class_="CardInfo__row CardInfo__row_ownersCount")
        car['owners'] = target.contents[1].text
    except:
        car['owners'] = np.nan
        
    try:
        target = soup.find('li', class_="CardInfo__row CardInfo__row_pts")
        car['PTS'] = target.contents[1].text
    except:
        car['PTS'] = np.nan
    
    try:
        target = soup.find('li', class_="CardInfoRow CardInfoRow_customs")
        car['customs'] = target.contents[1].text
    except:
        car['customs'] = np.nan
    
    try:
        target = soup.find('li', class_="CardInfoRow CardInfoRow_owningTime")
        car['owningTime'] = target.contents[1].text
    except:
        car['owningTime'] = np.nan
    
    try:
        car['id'] = int(soup.find('div', title="Идентификатор объявления").text.replace('№ ',''))
    except:
        car['id'] = np.nan

    # saving image
    filename = str(car['id'])+'.jpeg'
    try: 
        target = 'https://'+str(soup.find('img')['src'][2:])
        rr = requests.get(target, stream = True)

    
        with open('./saves/'+filename,'wb') as f:
            f.write(rr.content)
            f.close()
            print('Image sucessfully Downloaded: ',filename)
    except:
        print('Download failed:', filename)   
    return (car)


    
        
def parse_autoru(x):
    """General parsing function"""
    df = pd.DataFrame()
    url = 'https://auto.ru/moskva/cars/' + x + '/all/?page='
    for i in range(1,100):
        r = requests.get(url+str(i), headers={'User-Agent': 'Mozilla/5.0'})
        r.encoding = 'utf-8'
        main_soup = BeautifulSoup(r.text, 'html.parser')
        links = main_soup.find_all('a', class_="Link ListingItemTitle-module__link")
        for link in links:
            car = get_auto(link['href'])
            df = df.append(car, ignore_index = True)
            df.to_csv('./saves/backup.csv', mode='w')
            time.sleep(np.random.randint(1,10))
    return df

car_brands = ['bmw', 'audi', 'kia', 'ford', 'peaugeot', 'opel', 'skoda']

if __name__ == '__main__':
    for car in car_brands:
        data = parse_autoru(car)
        data.to_csv('./saves/' + car + '_train.csv', mode = 'w')
        time.sleep(np.random.randint(1,10))
