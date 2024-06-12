import streamlit as st
import sqlite3

st.title("IA - Mise à jour des catégories")

conn = sqlite3.connect('evenements.db')
c = conn.cursor()


if st.button('mise à jour des catégories'):
    c.execute('SELECT id FROM evenements WHERE cat1 IS NULL')
    rows = c.fetchall()
    cat1 = "'Concert'"
    cat2 = "'Famille'"
    cat3 = 'NULL'
    for row in rows:
        c.execute(f'''
                   UPDATE evenements
                      SET cat1 = {cat1},
                          cat2 = {cat2},
                          cat3 = {cat3}
                         WHERE id = {row[0]}
                  ''')
        conn.commit()
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
