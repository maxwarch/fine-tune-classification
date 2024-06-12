import streamlit as st
import sqlite3

st.title("Recherche d'évènements")
st.write("P.O.C.")

conn = sqlite3.connect('evenements.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS evenements (
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        cat1 TEXT,
        cat2 TEXT,
        cat3 TEXT
    )
''')

c.execute('SELECT * FROM evenements')
rows = c.fetchall()
st.write('Valeurs de texte dans la base de données :')
for row in rows:
    st.write(f'{row[0]} : {row[1]}')

conn.close()
