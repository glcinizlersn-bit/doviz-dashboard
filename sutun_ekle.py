# import sqlite3

# conn=sqlite3.connect("doviz.db")
# cursor=conn.cursor()

# #Değişim sütunu ekle 
# try:
#     cursor.execute("ALTER TABLE kurlar ADD COLUMN degisim TEXT")tabloya yeni bir sütun eklemek içidi 
#     print("✅ Sütun eklendi!")
# except:
#     print("Sütun zaten var")
# conn.commit()
# conn.close()

import sqlite3

conn = sqlite3.connect("doviz.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(kurlar)")
sutunlar = cursor.fetchall()

for sutun in sutunlar:
    print(sutun[1])

conn.close()