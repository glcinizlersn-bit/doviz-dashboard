from flask import Flask,redirect,request
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading 
import time


app = Flask(__name__)
# Döviz verilerini çekip kaydeden fonksiyon 
def veri_guncelle():
    conn = sqlite3.connect("doviz.db", timeout=10)
    cursor=conn.cursor()
    #Eski verileri sil
    cursor.execute("DELETE FROM kurlar")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name ='kurlar'")#sqlite_sequence → SQLite'ın id sayacını tuttuğu özel tablo. Bunu sıfırlayınca id tekrar 1'den başlar.
    #Yeni veri çek
    url ="https://www.doviz.com"
    headers={"User-Agent":"Mozilla/5.0"}
    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.text,"html.parser")
    dovizler=soup.find_all("div",class_="item")
    
    for doviz in dovizler:
        try:
            ad=doviz.find("span",class_="name").text.strip()
            fiyat=doviz.find("span",class_="value").text.strip()
            try:
                degisim=doviz.find("div",class_="change-rate").text.strip()
            except:
                degisim="0"
            cursor.execute("INSERT INTO kurlar (doviz,fiyat,degisim) VALUES (?,?,?)",(ad,fiyat,degisim))

        except:
            continue
    conn.commit()
    conn.close()
        #güncelleme zamanı dosyaya yaz
    with open ("son_guncelleme.txt","w") as f :
        f.write(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))# strftime:güzel formata taz 

def otomatik_guncelle():
    while True:
        time.sleep(300)#300 saniye =5 dakika oluyor
        print("Otomatik güncelleme yapılıyor...")
        veri_guncelle()
        print("✅ Otomatik güncellendi!")
    

    
@app.route("/")
def anasayfa():
    #Arama kelimesini al
    arama = request.args.get("arama", "") 
    conn = sqlite3.connect("doviz.db", timeout=10)
    cursor = conn.cursor()
    if arama:
        #Arama varsa filtrele 
        cursor.execute("SELECT * FROM kurlar WHERE doviz LIKE ?",('%'+arama+'%',))
    else:
     cursor.execute("SELECT * FROM kurlar")
    
    kurlar = cursor.fetchall()
    
    #grafik için veri hazırlama 
    grafik_isimler=[]
    grafik_fiyatlar=[]
    for kur in kurlar:
        grafik_isimler.append(kur[1])
        #FİYATI SAYIYA ÇEVİR (NOKTA VE VİRGÜL TEMİZLE)
        fiyat_temiz=kur[2].replace(".","").replace(",",".").replace("$","")
        try:
            grafik_fiyatlar.append(float(fiyat_temiz))
        except:
            grafik_fiyatlar.append(0)
    conn.close()

    #son gğncelleme zamanı oku 
    try:
        with open ("son_guncelleme.txt","r")as f:
            son_guncelleme=f.read()
    except:
        son_guncelleme="Henüz güncellenmedi"
    
    html = """
    <meta http-equiv="refresh" content="300">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <style>
        *{margin :0; box-sizing:border-box}
        body{
        font-family:'Segoe UI',Arial, sans-serif;
        background:linear-gradient(135deg,#667eea 0%, #764ba2 100%);
        padding:30px;
        color:#333;
    
    
        }
        .container{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);

        }
        h1{color: #333; margin-bottom:10px;}
        h2{color:#555; margin: 25px 0 15px;}
         .zaman{ color: #888; font-size: 14px; margin-bottom: 20px; }
         table { border-collapse: collapse; width: 100%; margin-top: 15px; display: block; overflow-x: auto; }
          th { 
            background: #667eea; color: white; padding: 15px; 
            text-align: left;
        }
        td { padding: 12px 15px; border-bottom: 1px solid #eee; }
        tr:hover { background: #f8f9ff; }
        .btn { 
            background: #667eea; color: white; padding: 12px 25px; 
            text-decoration: none; border-radius: 8px; display: inline-block;
            margin: 5px 5px 15px 0; transition: 0.3s;
        }
        .btn:hover { background: #5568d3; }
        input { 
            padding: 12px; width: 250px; border: 2px solid #ddd; 
            border-radius: 8px; font-size: 14px;
        }
        button { 
            padding: 12px 20px; background: #667eea; color: white; 
            border: none; border-radius: 8px; cursor: pointer;
        }
    </style>
     <div class="container">
    <h1>💱 Döviz Kurları</h1>
    <p>⏲Son güncelleme:"""+son_guncelleme+"""</p>
    <a href="/guncelle"class="btn">🎀 Verilleri Güncelle</a>
    <form method="get">
       <input type="text" name="arama" placeholder="Döviz Ara..." oninput="if(this.value=='') window.location='/'">
       <button type="submit">Ara</button>
    </form>
    <a href="/">Tümünü Göster</a>
    <table>
        <tr><th>ID</th><th>Döviz</th><th>Fiyat</th><th>Değişim</th></tr>
    """
    
    for kur in kurlar:
     degisim = kur[3]
     if degisim.startswith("%-"):
        renk = "red"
        ok = "⬇️"
     else:
        renk = "green"
        ok = "⬆️"
    
     html += f"<tr><td>{kur[0]}</td><td>{kur[1]}</td><td>{kur[2]}</td><td style='color:{renk}'>{ok} {degisim}</td></tr>"
    html += "</table>"
    #grafike ekle
    html+="""
    <h2>📊Fiyat Grafiği </h2>
    <canvas id ="grafik" width ="400" height="200"></canvas>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    const ctx=document.getElementById('grafik');
  new Chart (ctx,{
    type:'bar',
    data:{
        labels:""" +str(grafik_isimler)+""",
        datasets:[{
            label:'Fiyat',
            data:"""+str(grafik_fiyatlar)+""",
            backgroundColor:'#4472C4'
        }]
    },
    options:{
        scales:{
            y:{
                type:'logarithmic'
            }
        }
    }
    });
    
    </script>
"""
    html += "</div>"
    return html
@app.route("/guncelle")
def guncelle():
    veri_guncelle()
    return redirect("/")
if __name__ == "__main__":
    #Otomatik güncelemeyi arka planda başlat
    thread=threading.Thread(target=otomatik_guncelle,daemon=True)
    thread.start()
    app.run(debug=True)