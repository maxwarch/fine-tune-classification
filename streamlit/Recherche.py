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


cat1 = st.sidebar.selectbox("Catégorie 1", ('Action','Art','Atelier','Balade','Brocante','Concert','Conférence','Culture','Danse','Détente','Environnement','Exposition','Famille','Festival','Fête','Gastronomie','Histoire','Jeu','Marché','Santé','Spectacle','Sport','Théatre','Visite'))
cat2 = st.sidebar.selectbox("Catégorie 2", ('', 'Action','Art','Atelier','Balade','Brocante','Concert','Conférence','Culture','Danse','Détente','Environnement','Exposition','Famille','Festival','Fête','Gastronomie','Histoire','Jeu','Marché','Santé','Spectacle','Sport','Théatre','Visite'))
cat3 = st.sidebar.selectbox("Catégorie 3", ('', 'Action','Art','Atelier','Balade','Brocante','Concert','Conférence','Culture','Danse','Détente','Environnement','Exposition','Famille','Festival','Fête','Gastronomie','Histoire','Jeu','Marché','Santé','Spectacle','Sport','Théatre','Visite'))

print(f'''
          SELECT *
          FROM evenements
          WHERE cat1 = "{cat1}"
          ''')
c.execute(f'''
          SELECT *
          FROM evenements
          WHERE cat1 = "{cat1}"
          ''')
rows = c.fetchall()
st.write('Valeurs de texte dans la base de données :')
for row in rows:
    st.write(f'{row[0]} : {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}')

conn.close()
