# Airbnb Analytics Platform

## Présentation du projet
Ce projet est une plateforme d'analyse de données Airbnb utilisant une architecture de Modern Data Stack. L'objectif est de transformer des données brutes en informations lisibles et interactives concernant le parc immobilier, les performances des hôtes et l'analyse textuelle des avis utilisateurs.

## Répartition des tâches
* Data Engineering : Ouidad (Pipeline dbt & DuckDB)
* Data Visualisation : Fatima (Dashboard Streamlit)

## Installation et lancement (Windows)

1. Cloner le dépôt :
git clone https://github.com/boussalaouidad78-Fa/airbnb-analytics-platform.git

2. Créer et activer l'environnement virtuel :
python -m venv venv
venv\Scripts\activate

3. Installer les dépendances :
pip install dbt-duckdb duckdb streamlit pandas

4. Générer la base de données :
cd airbnb_analytics
dbt seed
dbt run
cd ..

5. Lancer le dashboard :
streamlit run app.py
