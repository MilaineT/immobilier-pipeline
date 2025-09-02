import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------
# 1. Charger les données
# -------------------

URL = "https://raw.githubusercontent.com/MilaineT/immobilier-pipeline/main/data/cleaned_data_final.csv"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(URL, sep=';', encoding="utf-8-sig", quotechar='"')
        
        if "location" not in df.columns:
            st.error(f"❌ Colonne 'location' non trouvée. Colonnes détectées : {df.columns.tolist()}")
            return pd.DataFrame()
        
        # Forcer la localisation en texte
        df["location"] = df["location"].astype(str)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {e}")
        return pd.DataFrame()

st.cache_data.clear()
df = load_data()

# -------------------
# Vérification du DataFrame
# -------------------
if df.empty:
    st.error("Le fichier CSV est vide ou introuvable.")
    st.stop()

# -------------------
# 2. Interface utilisateur
# -------------------

st.title("🏡 Tableau de bord immobilier")
st.write("Analyse des annonces immobilières")

# Filtres dynamiques
min_price, max_price = int(df["price_eur"].min()), int(df["price_eur"].max())
price_range = st.slider("Filtrer par prix (€)", min_price, max_price, (min_price, max_price))

min_surface, max_surface = int(df["surface_m2"].min()), int(df["surface_m2"].max())
surface_range = st.slider("Filtrer par surface (m²)", min_surface, max_surface, (min_surface, max_surface))

if "rooms_n" in df.columns:
    min_pieces, max_pieces = int(df["rooms_n"].min()), int(df["rooms_n"].max())
    pieces_range = st.slider("Filtrer par nombre de pièces", min_pieces, max_pieces, (min_pieces, max_pieces))
else:
    st.warning("Colonne 'rooms_n' absente du CSV.")
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
# 4. Visualisations
# -------------------

st.metric("💶 Prix moyen", f"{filtered['price_eur'].mean():,.0f} €")

# Histogramme prix avec étiquettes
fig_price_hist = px.histogram(filtered, x="price_eur", nbins=30, title="Répartition des prix")
fig_price_hist.update_traces(texttemplate="%{y}", textposition="outside")
st.plotly_chart(fig_price_hist)

# Tableau filtré
st.dataframe(filtered)

st.subheader("📊 Visualisations supplémentaires")

# Scatter Surface vs Prix
fig_scatter = px.scatter(
    filtered,
    x="surface_m2",
    y="price_eur",
    title="Surface vs Prix",
    labels={"surface_m2": "Surface (m²)", "price_eur": "Prix (€)"},
    color="rooms_n" if "rooms_n" in filtered.columns else None
)
st.plotly_chart(fig_scatter)

# -------------------
# Box, bar & count plots par localisation
# -------------------
if "location" in filtered.columns:
    # Distribution des prix par localisation
    fig_box = px.box(
        filtered,
        x="location",
        y="price_eur",
        title="Distribution des prix par localisation",
        labels={"location": "Localisation", "price_eur": "Prix (€)"}
    )
    st.plotly_chart(fig_box)

    # Prix moyen par localisation (avec étiquettes)
    prix_moyen_loc = filtered.groupby("location")["price_eur"].mean().sort_values(ascending=False)
    fig_bar_mean = px.bar(
        x=prix_moyen_loc.index,
        y=prix_moyen_loc.values,
        title="Prix moyen par localisation",
        labels={"x": "Localisation", "y": "Prix moyen (€)"}
    )
    fig_bar_mean.update_traces(text=prix_moyen_loc.values.round(0), textposition="outside")
    st.plotly_chart(fig_bar_mean)

    # Nombre d'annonces par localisation (avec étiquettes)
    annonces_par_loc = filtered["location"].value_counts().sort_values(ascending=False)
    fig_hist_count = px.bar(
        x=annonces_par_loc.index,
        y=annonces_par_loc.values,
        title="Nombre d'annonces par localisation",
        labels={"x": "Localisation", "y": "Nombre d'annonces"}
    )
    fig_hist_count.update_traces(text=annonces_par_loc.values, textposition="outside")
    st.plotly_chart(fig_hist_count)
else:
    st.warning("La colonne 'location' est absente des données filtrées.")