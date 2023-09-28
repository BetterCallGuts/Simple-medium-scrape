import requests
from bs4  import BeautifulSoup
import sqlite3
from datetime import datetime


res     = requests.get("https://medium.com/")
srccode = res.text
soup    = BeautifulSoup(srccode, "lxml")
headers = soup.find_all('a', {"class" : "bd be bf bg bh bi bj bk bl bm bn bo bp bq br"})
headers = headers[19:-11]
data_unc= []
counter = 1
a = 1
#get data loop
for i in headers:
    if counter %2 ==0:
        x= i.attrs['href']
        if x[0] != "/":
            res_2 = requests.get(str(x))
                    
            # data_unc.append(res_2.text)
            
        else:
            res_2   = requests.get(f"https://medium.com/{x}");
            src     = res_2.text
            soup    = BeautifulSoup(src, "lxml")
            tt      = ""
            article = soup.find_all("div", {"class" : "ab ca"})
            article = [o.text for o in article]
            for i in article:
                tt +=  " " + i +" "
            # print(tt)


            # print(res_2)
            data_unc.append({"ID" : a,"Author" : headers[counter -2].text , "Article" : tt})
    counter += 1
    a +=1

# print(data_unc)
con = sqlite3.connect("data.sqlite3");
curs= con.cursor()

day = datetime.today().day
month = datetime.today().month
year = datetime.today().year

curs.execute(f'''
CREATE TABLE IF NOT EXISTS day{str(day)}0{str(month)}0{year}DataArticle (
    Author text,
    Article text
);
''')

con.commit()
for i in data_unc:
    curs.execute(f'''
        INSERT INTO day{day}0{month}0{year}DataArticle VALUES ("{i["Author"]}", "{i["Article"]}")
    ''')
    con.commit()
authors = []
article = []

curs.close()
con.close()
a = 1
for s in data_unc:
    authors.append(s["Author"])
    article.append(s["Article"])
data = zip(authors, article)
print(*data)

