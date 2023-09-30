import requests
import json
import xlsxwriter
import time

#pip install requests
#pip install json
#pip install xlsxwriter
#pip install time


businessesInfoList = []

# def writeBusinessData:

def writeBusinessData(businessesInfoList):
    workbook = xlsxwriter.Workbook('businesses.xlsx')
    worksheet = workbook.add_worksheet()
    for row in range(len(businessesInfoList)):
        for col_num, info in enumerate(businessesInfoList[row]):
            worksheet.write(row , col_num, info)     

    workbook.close()

#def getBusinessData function that brings the data for a place by the place_ide

busiNum = 0

def getBusinessData(places_ids, businessNumber):
    
    for place_ide in places_ids:
        url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_ide}&fields=formatted_address,name,opening_hours,formatted_phone_number,website,price_level,url,reviews,photos&key=[your key]'
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data = json.loads(response.text)
        innerData = data['result']

        # checking for the existence of each field

        if('reviews' in innerData):
            reviews = []
            for rev in innerData['reviews']:
                review = rev['text']
                reviews.append(review)

            
            if len(reviews)==0:
                review1 = ""
                review2 = ""
                review3 = ""
            elif len(reviews)==1:
                review1 = reviews[0]
                review2 = ""
                review3 = ""
            elif len(reviews)==2:
                review1 = reviews[0]
                review2 = reviews[1]
                review3 = ""
            else:
                review1 = reviews[0]
                review2 = reviews[1]
                review3 = reviews[2]
        else:
            review1 = ""
            review2 = ""
            review3 = ""

        if('photos' in innerData):
            picutures = []
            for pic in innerData['photos']:
                picRef = pic['photo_reference']
                picUrl = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={picRef}&key=[your key]"
                picutures.append(picUrl)

            if len(picutures) == 0:
                photo1 = ""
                photo2 = ""
                photo3 = ""
            elif len(picutures) == 1:
                photo1 = picutures[0]
                photo2 = ""
                photo3 = ""
            elif len(picutures) == 2:
                photo1 = picutures[0]
                photo2 = picutures[1]
                photo3 = ""
            else:
                photo1 = picutures[0]
                photo2 = picutures[1]
                photo3 = picutures[2]
        else:
            photo1 = ""
            photo2 = ""
            photo3 = ""

        if('price_level' in innerData):
            price_level = innerData['price_level']
        else:
            price_level = ""
        
        if('url' in innerData):
            url = innerData['url']
        else:
            url=""

        if('website'in innerData):
            website = innerData['website']
        else:
            website = ""

        if('opening_hours'in innerData):
            opening_hours = " , ".join(innerData["opening_hours"]["weekday_text"])
        else:
            opening_hours = " "
        if('formatted_address'in innerData):
            formatted_address = innerData['formatted_address']
        else:
            formatted_address = innerData['formatted_address']

        if('formatted_phone_number' in innerData):
            formatted_phone_number = innerData['formatted_phone_number']
        else:
            formatted_phone_number = ""
        if('name'in innerData):
            name=innerData['name']
        else:
            name=""

        businessInfoList = [
            name,
            formatted_phone_number,
            formatted_address,
            opening_hours,
            website,
            url,
            price_level,
            photo1,
            photo2,
            photo3,
            review1,
            review2,
            review3
        ]
        global businessesInfoList
        businessesInfoList.append(businessInfoList)
    
    writeBusinessData(businessesInfoList)

def gestBusinessesNearBY(alt, longt, radious, lang, Btype,keywords,page_token=None):
    places_ids = []
    businessNumber = 0
    for i in range(3):
        time.sleep(2)
        if page_token is None:
            url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={alt},{longt}&radius={radious}&lang={lang}&type={Btype}&keyword={keywords}&key=[your key]'
        elif page_token is not None:
            url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={page_token}&key=[your key]'

        response = requests.request("GET", url)
        places = json.loads(response.text)['results']
        for place in places:
            places_ids.append(place['place_id'])
            businessNumber+=1
        if 'next_page_token' in json.loads(response.text):
            page_token = json.loads(response.text)['next_page_token']
        else:
            break
        
    getBusinessData(places_ids,businessNumber)


    
gestBusinessesNearBY(40.730610,	-73.935242,30000, 'en', ['retaurant','coffee shop'],'restaurant')

