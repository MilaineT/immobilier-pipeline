import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------
# 1. Charger les données
# -------------------

URL = "https://raw.githubusercontent.com/MilaineT/immobilier-pipeline/main/data/cleaned_data_final.csv"

#st.cache_data
def load_data():
    try:
        # Prise en compte des champs texte contenant des virgules
        df = pd.read_csv(URL, quotechar='"')
        df["location"] = df["location"].astype(str)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

# Nettoyage du cache pour recharger les données corrigées
st.cache_data.clear()
df = load_data()

# Vérifier si le DataFrame est vide
if df.empty:
    st.error("Le fichier CSV est vide ou introuvable.")
    st.stop()

# -------------------
# 2. Interface utilisateur
# -------------------

st.title("Tableau de bord immobilier")
st.write("Analyse des annonces immobilières")

# Filtres dynamiques
min_price, max_price = int(df["price_eur"].min()), int(df["price_eur"].max())
price_range = st.slider("Filtrer par prix (€)", min_price, max_price, (min_price, max_price))

min_surface, max_surface = int(df["surface_m2"].min()), int(df["surface_m2"].max())
surface_range = st.slider("Filtrer par surface (m²)", min_surface, max_surface, (min_surface, max_surface))

# Filtres nombre de pièces
if "rooms_n" in df.columns:
    min_pieces, max_pieces = int(df["rooms_n"].min()), int(df["rooms_n"].max())
    pieces_range = st.slider("Filtrer par nombre de pièces", min_pieces, max_pieces, (min_pieces, max_pieces))
else:
    st.warning("Colonne 'rooms_n' absente du CSV, filtre désactivé.")
    pieces_range = (0, 100)

# -------------------
# 3. Application des filtres
# -------------------

filtered = df[
    (df["price_eur"].between(*price_range)) &
    (df["surface_m2"].between(*surface_range))
]

if "rooms_n" in df.columns:
    filtered = filtered[filtered["rooms_n"].between(*pieces_range)]

# -------------------
# 4. Visualisations de base
# -------------------

# Prix moyen
st.metric("Prix moyen", f"{filtered['price_eur'].mean():,.0f} €")

# Histogramme des prix
fig_price_hist = px.histogram(filtered, x="price_eur", nbins=30, title="Répartition des prix")
st.plotly_chart(fig_price_hist)

# Tableau des données filtrées
st.dataframe(filtered)

# -------------------
# 5. Visualisations supplémentaires
# -------------------

st.subheader("Visualisations supplémentaires")

# 5.1 Nuage de points Surface vs Prix
fig_scatter = px.scatter(
    filtered,
    x="surface_m2",
    y="price_eur",
    title="Surface vs Prix",
    labels={"surface_m2": "Surface (m²)", "price_eur": "Prix (€)"},
    color="rooms_n" if "rooms_n" in filtered.columns else None
)
st.plotly_chart(fig_scatter)

# 5.2 Box plot du prix par localisation
if "location" in filtered.columns:
    fig_box = px.box(
        filtered,
        x="location",
        y="price_eur",
        title="Distribution des prix par localisation",
        labels={"location": "Localisation", "price_eur": "Prix (€)"}
    )
    st.plotly_chart(fig_box)

# 5.3 Prix moyen par localisation (bar plot)
if "location" in filtered.columns:
    prix_moyen_loc = filtered.groupby("location")["price_eur"].mean().sort_values(ascending=False)
    fig_bar_mean = px.bar(
        prix_moyen_loc,
        x=prix_moyen_loc.index,
        y=prix_moyen_loc.values,
        title="Prix moyen par localisation",
        labels={"x": "Localisation", "y": "Prix moyen (€)"}
    )
    st.plotly_chart(fig_bar_mean)

# 5.4 Nombre d’annonces par localisation
if "location" in filtered.columns:
    annonces_par_loc = filtered["location"].value_counts().sort_values(ascending=False)
    fig_hist_count = px.bar(
        x=annonces_par_loc.index,
        y=annonces_par_loc.values,
        title="Nombre d'annonces par localisation",
        labels={"x": "Localisation", "y": "Nombre d'annonces"}
    )
    st.plotly_chart(fig_hist_count)