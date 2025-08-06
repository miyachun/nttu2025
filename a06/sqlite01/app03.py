import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
print ("數據開啟成功")

cursor = c.execute("SELECT id, name, address, salary  from COMPANY")
for row in cursor:
   print ("ID = ", row[0])
   print ("NAME = ", row[1])
   print ("ADDRESS = ", row[2])
   print ("SALARY = ", row[3], "\n")

print ("資料查尋成功")
conn.close()