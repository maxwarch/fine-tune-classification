import urllib.parse
import streamlit as st
import sqlite3
import requests
import urllib


st.title("IA - Mise à jour des catégories")

conn = sqlite3.connect('evenements.db')
c = conn.cursor()


c.execute('SELECT * FROM ip')
row = c.fetchone()
ip = row[0]


api_url = f"http://{ip}:8001/predict?text="
if st.button('mise à jour des catégories'):
    c.execute('SELECT id, description FROM evenements WHERE cat1 IS NULL')
    rows = c.fetchall()

    for row in rows:
        url = f"{api_url}{urllib.parse.quote(row[1])}"
        response = requests.post(url)
        if response.status_code == 200:
            events = response.json()
            print(">>>>>>>>>>>>>>>>>", response, events)
            cat = [0,1,2]
            for index in range(3):
                label = events[index]['label']
                score = events[index]['score']
                if score >= 0.5:
                    cat[index] = f"'{label}'"
                else:
                    cat[index] = 'NULL'
                c.execute(f'''
                           UPDATE evenements
                              SET cat1 = {cat[0]},
                                  cat2 = {cat[1]},
                                  cat3 = {cat[2]}
                                 WHERE id = {row[0]}
                          ''')
                conn.commit()

        else:
            st.error("Erreur lors de la récupération des événements")
            events = []

    st.write('mise à jour effectuées')


# Afficher toutes les valeurs de texte dans la table
c.execute('''
          SELECT id, title, cat1, cat2, cat3
            FROM evenements
           WHERE cat1 IS NULL
           ORDER BY id DESC
          ''')
rows = c.fetchall()

for row in rows:
    st.write(f'{row[0]} > {row[1]} : {row[2]} | {row[3]} | {row[4]}')

conn.close()
