# Create stats.db for DisPong

import sqlite3 as sq

con = sq.connect("stats.db")
cur = con.cursor()

cur.execute("""CREATE TABLE main (totalgames int, currentgames int, ballspinged int, botgames int, rpsgames int, tttgames int)""")
cur.execute("""INSERT INTO main VALUES (0, 0, 0, 0, 0, 0)""")

con.commit()
con.close()
