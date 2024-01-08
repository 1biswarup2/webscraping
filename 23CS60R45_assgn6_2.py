import requests
import sqlite3
import json
from bs4 import BeautifulSoup
from random import sample 
import re
'''some times due to netwok error it is showing some error ; if it happens then just re-run'''
def getcount(info_table_rows1):
    for row in info_table_rows1:
      #if(row.th.text=='Athletes'):
      try:
         if(row.th.text=='Athletes'):
              return row.td.text
      except:
          continue
def getNations(tables1):
        nations1=[]
        for table in tables1:
            try:
                header1=table.tbody.tr.th.a.text
                #print(header1)
                if(header1=="National Olympic Committees"):
                    rows=table.tbody.find_all('tr')
                    for row in rows:
                        try:
                            lists=row.td.ul.find_all('li')
                            for li in lists:
                                nations1.append(li.a.text)
                        except:
                            continue
                    #print(name)
            except:
                continue
        return nations1
def getData(url,header):
    response = requests.get(url,headers=header)
    #convert to text string and return 
    return response.text
def getsports(all_divs):
    plays=[]
    for d in all_divs:
        rows1=d.find_all('tr')
        header=rows1[0].th
        #print(heading)
        if header is not None:
            heading=header.text
            print(heading)
            if 'Sports' in heading:
                c=rows1[1].td.div.table.tbody.tr
                cols=c.find_all('td')
                for col in cols:
                    sports=col.ul.find_all('li')
                    for sport in sports:
                        allaq=sport.text.split()
                        for aq in allaq:
                            plays.append(aq)
                        
                        # temp=sport.find('li').text
                        # print(temp)
        else:
         continue
    return  plays

def convertJson(data):
    return json.loads(data)

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur,con
def getcountry(ranks):
    rows=ranks[0].tbody.find_all('tr')
    countries=[]
    for row in rows:
        try:
            x=row.th.a
            countries.append(x.text)
        except:
            continue
    return countries
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
 'Accept-Language': 'en-US,en;q=0.9',
 'Accept-Encoding': 'gzip, deflate, br'}

url = 'https://en.wikipedia.org/wiki/Summer_Olympic_Games'
returnedData = getData(url,headers)
#print(returnedData)

dbName = "OlympicsData.db"
cursor,con = createDatabaseConnect(dbName)

query = "CREATE TABLE IF NOT EXISTS SummerOlympics(Name,WikipediaURL,Year,HostCity,ParticipatingNations,Athletes,Sports,Rank_1_nation,Rank_2_nation,Rank_3_nation)"
cursor.execute(query)

soup=BeautifulSoup(returnedData,'lxml')
para=soup.find_all('p')
links=[]
for p in para:
   for a in p.find_all('a'):
       links.append(a['href'])
#print(links)
olympic_link=[]
flag=0
for link in links:
    if 'Summer_Olympics' in link:
        olympic_link.append(link)

#print(olympic_link)
random_link=sample(olympic_link,2)
link1='https://en.wikipedia.org'+random_link[0]
link2='https://en.wikipedia.org'+random_link[1]

print(link1)
print(link2)

link1_data=getData(link1,headers)
soup1=BeautifulSoup(link1_data,'lxml')
soup2=BeautifulSoup(link1_data,'lxml')
name1=soup1.find('head').title.text
name2=soup1.find('head').title.text
year1=re.sub('_Summer_Olympics$', '', random_link[0])
year2=re.sub('_Summer_Olympics$', '', random_link[1])
print(year1[-4:])
print(year2[-4:])
host1=soup1.find('td',class_="infobox-data location").a.text
host2=soup1.find('td',class_="infobox-data location").a.text
print(host1)

tables1=soup1.find_all('table')
tables2=soup2.find_all('table')
nations1=getNations(tables1)
nations2=getNations(tables2)
'''for table in tables1:
    try:
       header1=table.tbody.tr.th.a.text
       print(header1)
       if(header1=="National Olympic Committees"):
           rows=table.tbody.find_all('tr')
           for row in rows:
               try:
                   lists=row.td.ul.find_all('li')
                   for li in lists:
                       nations1.append(li.a.text)
               except:
                   continue
           #print(name)
    except:
        continue
'''
#print(nations1)
info_table_rows1=soup1.find('table',class_="infobox").find_all('tr')
info_table_rows2=soup2.find('table',class_="infobox").find_all('tr')

participants1=getcount(info_table_rows1)
participants2=getcount(info_table_rows2)
print(participants1)

all_divs1=soup1.find_all('table',class_="wikitable")
plays1=getsports(all_divs1)
all_divs2=soup2.find_all('table',class_="wikitable")
plays2=getsports(all_divs2)
#print(all_divs)
plays1_str=','.join(plays1)
plays2_str=','.join(plays2)
   
print(plays1)      
ranks1=soup1.find_all('table',class_="wikitable sortable plainrowheaders jquery-tablesorter")
ranks2=soup2.find_all('table',class_="wikitable sortable plainrowheaders jquery-tablesorter")
top_cntry1=getcountry(ranks1)
top_cntry2=getcountry(ranks2)
#print(type(ranks1))

#print(top_cntry2)
# print(type(name1))
# print(type(link1))
# print(type(year1[-4:]))
# print(type(host1))
# print(type(nations1))
# print(type(participants1))
# print(type(plays))
# print(type(top_cntry1[0]))
nations1_str=','.join(nations1)
nations2_str=','.join(nations2)
#print(nations1_str)
query = "INSERT INTO SummerOlympics VALUES ('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s')"%(name1,link1,year1[-4:],host1,nations1_str,participants1,plays1_str,top_cntry1[0],top_cntry1[1],top_cntry1[2])
cursor.execute(query)
query = "INSERT INTO SummerOlympics VALUES ('%s', '%s', '%s','%s','%s','%s','%s','%s','%s','%s')"%(name2,link2,year2[-4:],host2,nations2_str,participants2,plays2_str,top_cntry2[0],top_cntry2[1],top_cntry2[2])
cursor.execute(query)
query = "SELECT * from SummerOlympics"
cursor.execute(query)
result=cursor.fetchall()
print(len(result))
for row in result:
    print(row)
query="SELECT year from SummerOlympics"
result=cursor.execute(query)
#result=cursor.fetch()
print("years are: ")
for e in result:
   print(e)
query="select ParticipatingNations from SummerOlympics"
result=cursor.execute(query)
sum=0
for nations in result:
    print(type(nations))
    sum=sum+len(str(nations).split(','))
print(f"avg number of partipating countries {sum/2}")
query="select Rank_1_nation,Rank_2_nation,Rank_3_nation from SummerOlympics"
cursor.execute(query)
result1=cursor.fetchall()
st1=set(result1[0])
st2=set(result1[1])
st3=st1.intersection(st2)
print(f"overlapping countries are: {st3}")