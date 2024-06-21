import streamlit as st
import sqlite3

st.title("MAJ IP")

conn = sqlite3.connect('evenements.db')
c = conn.cursor()

ip = st.text_input('IP :')

# Ajouter un nouveau bouton pour ajouter une valeur de texte
if st.button('Mise à jour'):
    c.execute(f'UPDATE ip SET ip = "{ip}"')
    conn.commit()

# Afficher toutes les valeurs de texte dans la table
c.execute('SELECT * FROM ip')
row = c.fetchone()
st.write(f"IP : {row[0]}")

conn.close()
