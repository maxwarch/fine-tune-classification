from math import floor
import streamlit as st
import sqlite3
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode


st.title("Recherche d'évènements")


conn = sqlite3.connect("evenements.db")
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS evenements (
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        cat1 TEXT,
        cat2 TEXT,
        cat3 TEXT,
        score1 REAL,
        score2 REAL,
        score3 REAL
    )
""")


c.execute("""
    CREATE TABLE IF NOT EXISTS ip (
        ip TEXT NOT NULL
    )
""")
c.execute("SELECT count(1) nb FROM ip")
row = c.fetchone()
if row[0] != 1:
    c.execute("DELETE FROM ip")
    c.execute('INSERT INTO ip VALUES ("0.0.0.0")')
    conn.commit()


cat1 = st.sidebar.selectbox(
    "Catégorie 1",
    (
        "",
        "Action",
        "Art",
        "Atelier",
        "Balade",
        "Brocante",
        "Concert",
        "Conférence",
        "Culture",
        "Danse",
        "Détente",
        "Environnement",
        "Exposition",
        "Famille",
        "Festival",
        "Fête",
        "Gastronomie",
        "Histoire",
        "Jeu",
        "Marché",
        "Santé",
        "Spectacle",
        "Sport",
        "Théatre",
        "Visite",
    ),
)
cat2 = st.sidebar.selectbox(
    "Catégorie 2",
    (
        "",
        "Action",
        "Art",
        "Atelier",
        "Balade",
        "Brocante",
        "Concert",
        "Conférence",
        "Culture",
        "Danse",
        "Détente",
        "Environnement",
        "Exposition",
        "Famille",
        "Festival",
        "Fête",
        "Gastronomie",
        "Histoire",
        "Jeu",
        "Marché",
        "Santé",
        "Spectacle",
        "Sport",
        "Théatre",
        "Visite",
    ),
)
cat3 = st.sidebar.selectbox(
    "Catégorie 3",
    (
        "",
        "Action",
        "Art",
        "Atelier",
        "Balade",
        "Brocante",
        "Concert",
        "Conférence",
        "Culture",
        "Danse",
        "Détente",
        "Environnement",
        "Exposition",
        "Famille",
        "Festival",
        "Fête",
        "Gastronomie",
        "Histoire",
        "Jeu",
        "Marché",
        "Santé",
        "Spectacle",
        "Sport",
        "Théatre",
        "Visite",
    ),
)

request = f"""
SELECT *
  FROM evenements
 WHERE ("{cat1}" = "" OR cat1 = "{cat1}" OR cat2 = "{cat1}" OR cat3 = "{cat1}")
   AND ("{cat2}" = "" OR cat1 = "{cat2}" OR cat2 = "{cat2}" OR cat3 = "{cat2}")
   AND ("{cat3}" = "" OR cat1 = "{cat3}" OR cat2 = "{cat3}" OR cat3 = "{cat3}")
"""
print(request)

c.execute(request)
rows = c.fetchall()

st.write(f"Nombre d'occurence dans la BDD : {len(rows)}")
col1, col2 = st.columns(2)
buttons = []

with col1:
    st.header("Liste des évènements")

    # for row in rows:
    #     st.write(f'{row[0]} : {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} {row[6]}')

    # Convertir les résultats en DataFrame
    df = pd.DataFrame(
        rows,
        columns=[
            "ID",
            "URL",
            "Titre",
            "Description",
            "Catégorie 1",
            "Catégorie 2",
            "Catégorie 3",
            "score1",
            "score2",
            "score3",
        ],
    )

    for row in rows:
        st.html(
            f"""{row[2]} 
                    <ul style="padding-left:30px">
                        <li>{row[4]}: {floor(row[7] * 100)}%</li>
                        <Li>{row[5]}: {floor(row[8] * 100)}%</li>
                        <li>{row[6]}: {floor(row[9] * 100)}%</li>
                    </ul>"""
        )
        buttons.append(st.button("Afficher", key=row[0]))


with col2:
    st.header("Informations")
    for index, button in enumerate(buttons):
        if button:
            row = rows[index]
            st.write(f"{row[1]}")
            st.write(f"{row[2]}")
            st.write(f"{row[4]} | {row[5]} | {row[6]}")
            st.write(f"{row[3]}")


conn.close()
