import sqlite3

con = sqlite3.connect("Highscores.db")
cursor = con.cursor()
queryTable = "CREATE TABLE Highscores (" \
             "ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
             "Ime TEXT, " \
             "Points INTEGER )"

cursor.execute(queryTable)
con.commit()
con.close()
