import requests
import sqlite3
import json
from bs4 import BeautifulSoup
def getData(url):
    response = requests.get(url)
    #convert to text string and return 
    return response.text

def convertJson(data):
    return json.loads(data)

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur,con
country='india'
limit='5'
API='352d48781b3d89f88e69f3a49e48a19f'
#returnedData = getData(url)
lat=[44,45,50,55,60]
lon=[22,46,38,39,56]
for k in range(len(lat)):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat[k]}&lon={lon[k]}&appid={API}"
    ).text
    jsonresponse=json.loads(response)
    need=['name',]
    city=jsonresponse["name"]
    temp=jsonresponse["main"]["temp"]
    weather=jsonresponse["weather"][0]["description"]
    humidity=jsonresponse["main"]["humidity"]
    wspeed=jsonresponse["wind"]["speed"]
    print(jsonresponse["name"])
    print(jsonresponse["main"]["temp"])
    print(jsonresponse["weather"][0]["description"])
    print(jsonresponse["main"]["humidity"])
    print(jsonresponse["wind"]["speed"])

    dbName = "Weather.db"
    cursor,con = createDatabaseConnect(dbName)

    query = "CREATE TABLE IF NOT EXISTS city_weather(City,Temperature,Description,Humidity,WindSpeed)"
    cursor.execute(query)
    query = "INSERT INTO city_weather VALUES ('%s', '%f', '%s','%f','%d')"%(city,temp,weather,humidity,wspeed)
    cursor.execute(query)
    query = "SELECT * from city_weather"

    cursor.execute(query)
    result=cursor.fetchall()
    print(len(result))
    for row in result:
        print(row)
    con.commit()
    cursor.close()