import sqlite3
conn =sqlite3.connect("data.db")
cursor=conn.cursor()

#YENİ TABLO OLUŞTUR (İD OTOMATİK ARTACAK)
# cursor.execute("""
#     CREATE TABLE  kisiler(
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         isim TEXT,
#         yas INTEGER,
#         sehir TEXT
#     )

#  """
#  )
 # cursor.execute("INSERT INTO kisiler (isim ,yas,sehir ) VALUES (?,?,?)",("Ahmet",25,"izmir"))
# cursor.execute("INSERT INTO kisiler (isim ,yas,sehir ) VALUES (?,?,?)",("Ayşe",30,"istanbul"))
# cursor.execute("INSERT INTO kisiler (isim ,yas,sehir ) VALUES (?,?,?)",("Mehmet",30,"ankara"))


# conn.commit()
# print ("✅Veriler eklendi!")

#YAŞI 28 DEN BÜYÜK OLANLARI 
cursor.execute("SELECT *FROM kisiler WHERE yas >28")
sonuc=cursor.fetchall()#sonuçları al  (fetchall tüm sonuçları getir demek )
# fetchall() → tüm satırları getir
# fetchone() → sadece ilk satırı getir
# fetchmany(5) → 5 satır getir
for kisi in sonuc:
    print(kisi)

conn.close()