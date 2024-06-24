from pathlib import Path
import urllib.parse
import streamlit as st
import sqlite3
import requests
import urllib
from dotenv import load_dotenv
import os


ENV = ".env"
BASE_DIR = Path(__file__).absolute()
load_dotenv(os.path.join(BASE_DIR.parent.parent, ENV))
cle = os.environ.get("CLE")

st.title("IA - Mise à jour des catégories")

conn = sqlite3.connect("evenements.db")
c = conn.cursor()


# obsolète
# c.execute('SELECT * FROM ip')
# row = c.fetchone()
# ip = row[0]


# récupération de l'IP
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {cle}",
    "X-GitHub-Api-Version": "2022-11-28",
}

response = requests.get(
    "https://api.github.com/repos/maxwarch/fine-tune-classification/actions/variables",
    headers=headers,
)
if response.status_code == 200:
    events = response.json()
    ip = events["variables"][0]["value"]
    print(">>>>>>>>>>IP>>>>>", ip)

api_url = f"http://{ip}:8001/predict?text="
if st.button("mise à jour des catégories"):
    c.execute("SELECT id, description FROM evenements WHERE cat1 IS NULL")
    rows = c.fetchall()

    for row in rows:
        url = f"{api_url}{urllib.parse.quote(row[1])}"
        response = requests.post(url)
        if response.status_code == 200:
            events = response.json()

            cat = [0, 1, 2]
            sco = [0, 1, 2]
            for index in range(3):
                label = events[index]["label"]
                score = events[index]["score"]

                if score >= 0.5:
                    cat[index] = f"'{label}'"
                    sco[index] = f"'{score}'"
                else:
                    cat[index] = "NULL"
                    sco[index] = -1
                c.execute(f"""
                           UPDATE evenements
                              SET cat1 = {cat[0]},
                                  cat2 = {cat[1]},
                                  cat3 = {cat[2]},
                                  score1 = {sco[0]},
                                  score2 = {sco[1]},
                                  score3 = {sco[2]}
                                 WHERE id = {row[0]}
                          """)
                conn.commit()

        else:
            st.error("Erreur lors de la récupération des événements")
            events = []

    st.write("mise à jour effectuées")


# Afficher toutes les valeurs de texte dans la table
c.execute("""
          SELECT id, title, cat1, cat2, cat3
            FROM evenements
           WHERE cat1 IS NULL
           ORDER BY id DESC
          """)
rows = c.fetchall()

for row in rows:
    st.write(f"{row[0]} > {row[1]} : {row[2]} | {row[3]} | {row[4]}")

conn.close()
