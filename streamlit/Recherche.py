import streamlit as st
import sqlite3
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


st.title("Recherche d'évènements")


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

c.execute('''
    CREATE TABLE IF NOT EXISTS ip (
        ip TEXT NOT NULL
    )
''')
c.execute('SELECT count(1) nb FROM ip')
row = c.fetchone()
if row[0] != 1:
    c.execute('DELETE FROM ip')
    c.execute('INSERT INTO ip VALUES ("0.0.0.0")')
    conn.commit()


cat1 = st.sidebar.selectbox("Catégorie 1", ('', 'Action','Art','Atelier','Balade','Brocante','Concert','Conférence','Culture','Danse','Détente','Environnement','Exposition','Famille','Festival','Fête','Gastronomie','Histoire','Jeu','Marché','Santé','Spectacle','Sport','Théatre','Visite'))
cat2 = st.sidebar.selectbox("Catégorie 2", ('', 'Action','Art','Atelier','Balade','Brocante','Concert','Conférence','Culture','Danse','Détente','Environnement','Exposition','Famille','Festival','Fête','Gastronomie','Histoire','Jeu','Marché','Santé','Spectacle','Sport','Théatre','Visite'))
cat3 = st.sidebar.selectbox("Catégorie 3", ('', 'Action','Art','Atelier','Balade','Brocante','Concert','Conférence','Culture','Danse','Détente','Environnement','Exposition','Famille','Festival','Fête','Gastronomie','Histoire','Jeu','Marché','Santé','Spectacle','Sport','Théatre','Visite'))

request = f'''
SELECT *
  FROM evenements
 WHERE ("{cat1}" = "" OR cat1 = "{cat1}" OR cat2 = "{cat1}" OR cat3 = "{cat1}")
   AND ("{cat2}" = "" OR cat1 = "{cat2}" OR cat2 = "{cat2}" OR cat3 = "{cat2}")
   AND ("{cat3}" = "" OR cat1 = "{cat3}" OR cat2 = "{cat3}" OR cat3 = "{cat3}")
'''
print(request)

c.execute(request)
rows = c.fetchall()
st.write(f"Nombre d'occurence dans la BDD : {len(rows)}")

# for row in rows:
#     st.write(f'{row[0]} : {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}')

# Convertir les résultats en DataFrame
s.write('avant DF')
df = pd.DataFrame(rows, columns=['ID', 'URL', 'Titre', 'Description', 'Catégorie 1', 'Catégorie 2', 'Catégorie 3'])
s.write('après DF')

# Configurer AgGrid
gb = GridOptionsBuilder.from_dataframe(df[['Titre', 'Catégorie 1', 'Catégorie 2', 'Catégorie 3']])
gb.configure_selection('single', use_checkbox=True, groupSelectsChildren=True)
gridOptions = gb.build()

# Afficher les résultats dans un tableau interactif
grid_response = AgGrid(
    df,
    gridOptions=gridOptions,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=True,
    height=350,
    width='100%',
)

# Récupérer les données de la ligne sélectionnée
selected_rows = grid_response['selected_rows']

if selected_rows is not None:
    st.subheader("Détails de l'évènement sélectionné")
    st.text(f"[{selected_rows.iloc[0][0]}] {selected_rows.iloc[0][1]}")
    st.text(f"{selected_rows.iloc[0][2]}")
    st.write(f"{selected_rows.iloc[0][3]}")
    


conn.close()
