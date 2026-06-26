import sqlite3
import requests
from bs4 import BeautifulSoup

#VERİTABANI HAZIRLA 
conn=sqlite3.connect("doviz.db")
cursor=conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS kurlar(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               doviz TEXT ,
               fiyat TEXT
        
        )
 """)

#VERİLERİ ÇEKECEZ
url= "https://www.doviz.com"
headers={"User-Agent":"Mozilla/5.0"}
response =requests.get(url, headers=headers)
soup=BeautifulSoup(response.text,"html.parser")
dovizler=soup.find_all("div",class_="item")
print(f"Bulunan döviz sayısı: {len(dovizler)}")

#VERİTABANINA KAYDET
for doviz in dovizler:
    try:
        ad=doviz.find("span",class_="name").text.strip()
        fiyat=doviz.find("span",class_="value").text.strip()
        cursor.execute("INSERT INTO kurlar (doviz,fiyat)VALUES(?,?)",(ad, fiyat))
        print(f"{ad}→{fiyat}kaydedildi")
    except:
        continue
conn.commit()
conn.close()
print("✅Tüm veriler veritabanına kaydedildi!")
