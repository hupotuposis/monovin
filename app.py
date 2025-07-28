import streamlit as st
import numpy as np
import math

st.set_page_config(layout="wide")
st.title("🎯 Vincent's Interactive Activity Circle")

# Initialiser les activités
if "activities" not in st.session_state:
    st.session_state.activities = [
        {"name": "Joseph Prince", "color": "#87CEEB", "aspects": ["Traduction", "Alignement biblique", "Delivery voix"]},
        {"name": "Vox Dubbing", "color": "#00BFFF", "aspects": ["Formation comédiens", "Direction artistique", "Qualité livrables"]},
        {"name": "TTL & Taxes", "color": "#FF6666", "aspects": ["Factures", "Déclarations", "Suivi MRA"]},
        {"name": "Podcast Léon", "color": "#FFA500", "aspects": ["Voix", "Montage", "Effets sonores"]},
        {"name": "Animation / MC", "color": "#90EE90", "aspects": ["Planning", "Prépa fiche", "Évènements à venir"]},
        {"name": "Projet Agricole", "color": "#DAA520", "aspects": ["Plantation", "Subventions", "Entretien"]},
        {"name": "Vie spirituelle", "color": "#BA55D3", "aspects": ["Temps personnel", "Journaux", "Prières"]},
        {"name": "Temps famille", "color": "#ADD8E6", "aspects": ["Savannah & Hugo", "Week-ends", "Aventures"]},
    ]

activities = st.session_state.activities
n = len(activities)

# Simuler un cercle de boutons
st.subheader("🧭 Cliquez sur un domaine pour explorer")
columns = st.columns(3)

clicked = None
for i in range(n):
    angle = 2 * math.pi * i / n
    raw_index = int((math.sin(angle) + 1) * 1.5)
    col_index = max(0, min(raw_index, 2))  # sécurité pour rester entre 0 et 2
    with columns[col_index]:
        if st.button(activities[i]["name"], key=f"activity_{i}"):
            clicked = activities[i]

# Affichage du domaine sélectionné
if clicked:
    st.markdown(f"## 🧩 Détails de **{clicked['name']}**")
    for asp in clicked["aspects"]:
        st.markdown(f"- {asp}")

# Ajouter / modifier des domaines
st.divider()
st.subheader("➕ Ajouter ou modifier un domaine")
with st.form("add_activity"):
    name = st.text_input("Nom du domaine")
    color = st.color_picker("Couleur")
    aspects = st.text_area("Liste des aspects (1 par ligne)")
    submitted = st.form_submit_button("Ajouter / Mettre à jour")

if submitted and name:
    existing = next((a for a in activities if a["name"] == name), None)
    aspect_list = [a.strip() for a in aspects.splitlines() if a.strip()]
    if existing:
        existing["color"] = color
        existing["aspects"] = aspect_list
        st.success(f"✅ Domaine mis à jour : {name}")
    else:
        activities.append({"name": name, "color": color, "aspects": aspect_list})
        st.success(f"✅ Domaine ajouté : {name}")

# Supprimer
st.subheader("🗑️ Supprimer un domaine")
to_delete = st.selectbox("Choisir un domaine à supprimer", [a["name"] for a in activities])
if st.button("Supprimer ce domaine"):
    st.session_state.activities = [a for a in activities if a["name"] != to_delete]
    st.success(f"❌ Domaine supprimé : {to_delete}")
