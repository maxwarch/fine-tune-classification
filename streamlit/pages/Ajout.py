import streamlit as st
import sqlite3

st.title("Ajout")

conn = sqlite3.connect('evenements.db')
c = conn.cursor()

url = st.text_input('URL :')
titre = st.text_input('Titre :')
description = st.text_input('Description :')

# Ajouter un nouveau bouton pour ajouter une valeur de texte
if st.button('Ajouter'):
    c.execute('''
              INSERT INTO evenements (url, title, description)
                   VALUES (?,?,?)
              ''', (url,titre,description))
    conn.commit()

# Afficher toutes les valeurs de texte dans la table
c.execute('SELECT * FROM evenements ORDER BY id DESC')
rows = c.fetchall()

for row in rows:
    st.write(f'{row[0]} : {row[2]}')

conn.close()
