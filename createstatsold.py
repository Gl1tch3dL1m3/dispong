# Create stats.db for DisPong Classic

import sqlite3 as sq

con = sq.connect("stats.db")
cur = con.cursor()

cur.execute("""CREATE TABLE main (totalgames int, currentgames int, ballspinged int, botgames int)""")
cur.execute("""INSERT INTO main VALUES (0, 0, 0, 0)""")

con.commit()
con.close()
