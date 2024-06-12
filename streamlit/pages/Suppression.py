import streamlit as st
import sqlite3

st.title("Suppression")

conn = sqlite3.connect('evenements.db')
c = conn.cursor()

c.execute('SELECT * FROM evenements')
rows = c.fetchall()

# Créer une liste de cases à cocher pour chaque ligne
selected_rows = st.multiselect('Sélectionnez les lignes à supprimer :', [f'{row[1]} : {row[2]}' for row in rows])

# Supprimer les lignes sélectionnées
if st.button('Supprimer les lignes sélectionnées'):
    for row_id in [int(row_id_str.split(' :')[0]) for row_id_str in selected_rows]:
        c.execute('DELETE FROM evenements WHERE id=?', (row_id,))
    conn.commit()

    # Mettre à jour l'affichage des valeurs de texte restantes
    c.execute('SELECT * FROM evenements')
    rows = c.fetchall()
    st.write('Valeurs de texte dans la base de données :')
    for row in rows:
        st.write(f'{row[0]} : {row[1]}')

conn.close()
