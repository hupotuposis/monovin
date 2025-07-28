import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Interface pour éditer les tâches
st.set_page_config(layout="wide")
st.title("🎲 Vincent's Interactive Monopoly Board")

st.subheader("✍️ Modifier, ajouter ou supprimer une activité")

if "tiles" not in st.session_state:
    st.session_state.tiles = [
        {"name": "Home", "color": "lightgray"},
        {"name": "Joseph Prince Translation", "color": "skyblue", "urgent": True},
        {"name": "Vox Dubbing Studio", "color": "skyblue"},
        {"name": "TTL Admin & Taxes", "color": "red", "urgent": True},
        {"name": "Podcast Léon", "color": "skyblue"},
        {"name": "MC & Event Hosting", "color": "lightgreen"},
        {"name": "Agriculture Project", "color": "lightyellow"},
        {"name": "MyFamilyGrocer Advertising", "color": "orange"},
        {"name": "Green Gears Invoice", "color": "red", "urgent": True},
        {"name": "IBL DodoTrail Invoice", "color": "red", "urgent": True},
        {"name": "CentrePoint Ad", "color": "orange"},
        {"name": "Galaxy Event Planning", "color": "lightgreen"},
        {"name": "Airbnb Planning", "color": "pink"},
        {"name": "Weekend with Kids", "color": "lightblue"},
        {"name": "Jesuis Project", "color": "violet"},
        {"name": "Spiritual Growth", "color": "violet"},
    ]

tiles = st.session_state.tiles

# Réordonner les activités
st.subheader("📦 Réorganiser les activités")
order = st.selectbox("Choisir une activité à déplacer", [tile["name"] for tile in tiles])
move_dir = st.radio("Déplacer :", ["Vers le haut", "Vers le bas"], horizontal=True)
if st.button("Appliquer le déplacement"):
    idx = next((i for i, t in enumerate(tiles) if t["name"] == order), None)
    if idx is not None:
        if move_dir == "Vers le haut" and idx > 0:
            tiles[idx], tiles[idx-1] = tiles[idx-1], tiles[idx]
        elif move_dir == "Vers le bas" and idx < len(tiles) - 1:
            tiles[idx], tiles[idx+1] = tiles[idx+1], tiles[idx]

# Formulaire d'ajout ou de mise à jour
with st.form("edit_form"):
    new_name = st.text_input("Nom de l'activité")
    new_color = st.color_picker("Couleur de la case", value="#87CEEB")
    new_urgent = st.checkbox("Est-ce urgent ?")
    submit = st.form_submit_button("Ajouter / Mettre à jour")

if submit and new_name:
    found = False
    for tile in tiles:
        if tile["name"] == new_name:
            tile["color"] = new_color
            tile["urgent"] = new_urgent
            found = True
            break
    if not found:
        tiles.append({"name": new_name, "color": new_color, "urgent": new_urgent})
    st.success(f"Activité '{new_name}' ajoutée ou mise à jour.")

# Suppression d'activité
st.subheader("🗑️ Supprimer une activité")
to_delete = st.selectbox("Choisir une activité à supprimer", [tile["name"] for tile in tiles])
if st.button("Supprimer"):
    tiles[:] = [tile for tile in tiles if tile["name"] != to_delete]
    st.success(f"Activité '{to_delete}' supprimée.")

# Sélection d'une case
selected_tile = st.selectbox("Choisissez une activité pour voir les conseils", [tile["name"] for tile in tiles])

urgent_tiles = [tile["name"] for tile in tiles if tile.get("urgent")]

if selected_tile:
    st.subheader(f"📌 Activité : {selected_tile}")
    if selected_tile in urgent_tiles:
        st.error("🚨 Cette tâche est URGENTE. Traitez-la dès que possible.")
    else:
        st.info("📅 Cette tâche peut être planifiée selon vos disponibilités.")

# Affichage du plateau
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_aspect('equal')
ax.axis('off')

positions = [(x, 0) for x in range(10)] + [(9, y) for y in range(1, 10)] + [(x, 9) for x in range(8, -1, -1)] + [(0, y) for y in range(8, 0, -1)]

for i, (x, y) in enumerate(positions[:len(tiles)]):
    tile = tiles[i]
    rect = patches.Rectangle((x, y), 1, 1, linewidth=1, edgecolor='black', facecolor=tile["color"])
    ax.add_patch(rect)
    ax.text(x + 0.5, y + 0.5, tile["name"], ha='center', va='center', fontsize=6, wrap=True)
    if tile.get("urgent"):
        ax.text(x + 0.5, y + 0.2, "URGENT", ha='center', va='center', fontsize=8, color='red', fontweight='bold')

st.pyplot(fig)

st.caption("Cliquez sur une activité en haut pour voir les priorités et conseils. Vous pouvez aussi ajouter, modifier, réordonner ou supprimer des cases.")
