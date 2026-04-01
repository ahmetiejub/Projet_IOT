import sqlite3

conn = sqlite3.connect('projet_iot.db')
cursor = conn.cursor()

print("--- CONTENU DE LA BASE DE DONNÉES ---")
try:
    cursor.execute("SELECT * FROM scores")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
except Exception as e:
    print("Erreur ou table vide :", e)

conn.close()