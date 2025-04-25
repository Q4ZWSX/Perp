import sqlite3
import sys

machine = sys.argv[1]
flag1 = sys.argv[2]
flag2 = sys.argv[3]

conn = sqlite3.connect('/app/database.db')
cursor = conn.cursor()
cursor.execute("UPDATE flags SET flag = ? WHERE machine = ? AND location = '/tmp/flag.txt'", (flag1, machine))
cursor.execute("UPDATE flags SET flag = ? WHERE machine = ? AND location = '/root/flag.txt'", (flag2, machine))
conn.commit()
conn.close()
