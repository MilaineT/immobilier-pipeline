# Création d'un pipeline de données  
## Analyse du marché de l'immobilier

###  Objectif  
Mettre en place un pipeline automatisé pour analyser des annonces immobilières : génération/simulation des données, nettoyage et visualisation via Streamlit.

- **GitHub** : [https://github.com/MilaineT/immobilier-pipeline](https://github.com/MilaineT/immobilier-pipeline/tree/main)  
- **Dashboard (public)** : [https://immobilier-pipeline-w4q3j4yyk9ze7igeqydjhq.streamlit.app/](https://immobilier-pipeline-w4q3j4yyk9ze7igeqydjhq.streamlit.app/)

---

### Implémentation

#### 1. Extraction (simulation de scraping) — `src/spider.py`  
Un spider (`spider.py`) a été développé pour collecter des informations clés sur les biens immobiliers :  
prix, surface, localisation, nombre de pièces.

#### 2. Nettoyage & préparation — `src/cleaner.py`  
- Conversion des champs numériques (`price_eur`, `surface_m2`)
- Calcul de `price_per_m2`
- Export au format CSV : `data/cleaned_data_final.csv` (encodage UTF-8-SIG, séparateur `;`)

#### 3. Automatisation — GitHub Actions  
Un workflow GitHub Actions est déclenché :
- à chaque `push`
- tous les jours à 09:00 UTC (`cron`)
- manuellement

Il exécute les traitements et pousse les fichiers CSV mis à jour dans le dépôt.

#### 4. Visualisation — `app.py` (Streamlit + Plotly)  
- Lecture du fichier CSV depuis GitHub (format brut/raw)
- Filtres interactifs : prix, surface, nombre de pièces
- KPI : prix moyen
- Graphiques : histogramme des prix, scatter plot (surface vs prix), boxplots/barres par localisation
- Tableau filtrable

---

###  Dépendances  
Fichier `requirements.txt` pour l'installation des dépendances nécessaires à l'application.

---

