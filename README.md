CREATION D'UN PIPELINE DE DONNEES
Analyse du Marché de l’Immobilier

But  
Mettre en place un pipeline automatisé pour analyser des annonces immobilières : génération/simulation des données, nettoyage et visualisation via Streamlit.

Github: https://github.com/MilaineT/immobilier-pipeline/tree/main
Dashboard (public) : https://immobilier-pipeline-w4q3j4yyk9ze7igeqydjhq.streamlit.app/


Implémentation:

- Extraction (simulation de scraping)— `src/spider.py`  
  Un spider (fichier spider.py) a été développé pour collecter des informations clés sur les biens immobiliers (prix, surface, localisation, nombre de pièces)

- Nettoyage & préparation — `src/cleaner.py`  
  Conversions numériques (`price_eur`, `surface_m2`), calcul `price_per_m2`, export `data/cleaned_data_final.csv` (UTF-8-SIG, `;`).

- Automatisation — GitHub Actions  
  Workflow déclenché à chaque push, quotidiennement (cron 09:00 UTC) et manuellement : exécute le traitement et commit/push les CSV mis à jour.

- Visualisation — `app.py` (Streamlit + Plotly)  
  Lecture du CSV depuis GitHub (raw), filtres prix / surface / pièces, KPI (prix moyen), histogramme des prix, scatter Surface↔Prix, box/bar par localisation, tableau filtrable.
  requirement.txt pour l’installation des dépendances