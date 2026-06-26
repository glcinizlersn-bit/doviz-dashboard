import sqlite3
 #veritabanına bağlan yoksa oluştur

conn=sqlite3.connect("test.db")

#cursor oluştur (sorgu oluşturmak için )
cursor=conn.cursor()

#tablo oluştur

# cursor.execute("""
# CREATE TABLE IF NOT EXİSTS kisiler(
#     id INTEGER PRİMARY KEY,
#     isim TEXT,
#     yas INTEGER,
#     sehir TEXT

# )
# """
# )
#kişileri ekleme
# cursor.execute("INSERT INTO kisiler (isim,yas,sehir) VALUES(?,?,?)",("Ahmet",25,"İzmir"))
# cursor.execute("INSERT INTO kisiler (isim,yas,sehir) VALUES(?,?,?)",("Ayşe",30,"İstanbul"))
# cursor.execute("INSERT INTO kisiler (isim,yas,sehir) VALUES(?,?,?)",("Mehmet",28,"Ankara"))

#ksorgulamak için 
# cursor.execute("SELECT * FROM kisiler")
# kisiler=cursor.fetchall()
# for kisi in kisiler:
#     print(kisi)

#tüm verileri sil 
#cursor.execute("DELETE FROM kisiler")
conn.commit()
print("✅Veriler eklendi")

conn.close()


