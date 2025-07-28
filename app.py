import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(layout="wide")
st.title("🔵 Vincent's Activity Sphere")

# Initialiser les activités principales si besoin
if "activities" not in st.session_state:
    st.session_state.activities = [
        {"name": "Joseph Prince", "color": "#87CEEB", "aspects": ["Traduction", "Alignement biblique", "Delivery voix"]},
        {"name": "Vox Dubbing", "color": "#00BFFF", "aspects": ["Formation comédiens", "Direction artistique", "Qualité livrables"]},
        {"name": "TTL & Taxes", "color": "#FF6666", "aspects": ["Factures", "Déclarations", "Suivi MRA"]},
        {"name": "Podcast Léon", "color": "#FFA500", "aspects": ["Voix", "Montage", "Effets sonores"]},
        {"name": "Animation / MC", "color": "#90EE90", "aspects": ["Planning", "Prépa fiche", "Évènement à venir"]},
        {"name": "Projet Agricole", "color": "#DAA520", "aspects": ["Plantation", "Subventions", "Entretien"]},
        {"name": "Vie spirituelle", "color": "#BA55D3", "aspects": ["Temps personnel", "Journaux", "Prières"]},
        {"name": "Temps famille", "color": "#ADD8E6", "aspects": ["Savannah & Hugo", "Week-ends", "Aventures"]},
    ]

activities = st.session_state.activities

# Affichage en cercle
st.subheader("🌐 Vue sphérique des domaines d’activité")
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_aspect('equal')
ax.axis('off')

n = len(activities)
radius = 1
angles = np.linspace(0, 2 * np.pi, n, endpoint=False)

positions = [(radius * np.cos(a), radius * np.sin(a)) for a in angles]
for i, (x, y) in enumerate(positions):
    activity = activities[i]
    ax.add_patch(plt.Circle((x, y), 0.2, color=activity["color"], ec='black'))
    ax.text(x, y, activity["name"], ha='center', va='center', fontsize=8, wrap=True)

# Centre
ax.add_patch(plt.Circle((0, 0), 0.25, color='gray', ec='black'))
ax.text(0, 0, "Moi", ha='center', va='center', fontsize=10, fontweight='bold')

st.pyplot(fig)

# Interaction
st.subheader("🔍 Explorer un domaine")
selected = st.selectbox("Choisissez un domaine", [a["name"] for a in activities])

for a in activities:
    if a["name"] == selected:
        st.markdown(f"### 🧩 Détails de **{a['name']}**")
        for aspect in a["aspects"]:
            st.markdown(f"- {aspect}")

# Ajouter / modifier des domaines et aspects
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
        st.success(f"Domaine {name} mis à jour.")
    else:
        activities.append({"name": name, "color": color, "aspects": aspect_list})
        st.success(f"Domaine {name} ajouté.")

# Supprimer un domaine
st.subheader("🗑️ Supprimer un domaine")
to_delete = st.selectbox("Choisir un domaine à supprimer", [a["name"] for a in activities])
if st.button("Supprimer ce domaine"):
    st.session_state.activities = [a for a in activities if a["name"] != to_delete]
    st.success(f"Domaine {to_delete} supprimé.")
