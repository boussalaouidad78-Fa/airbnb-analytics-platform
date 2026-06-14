# Airbnb Analytics Platform

## Présentation du projet
Ce projet est réalisé dans le cadre de notre évaluation de MBA Big Data & IA. Il s'agit d'une plateforme d'analyse de données Airbnb utilisant une architecture de Modern Data Stack. 
L'objectif est de transformer des données brutes en informations lisibles et interactives concernant le parc immobilier, les performances des hôtes et l'analyse textuelle des avis utilisateurs.

## Répartition des tâches
* **Data Engineering (Pipeline dbt & DuckDB) :** Ouidad
  * Architecture et création des couches Bronze (brutes), Silver (nettoyées) et Gold (prêtes à l'emploi) via des modèles dbt.
* **Data Visualisation (Application Streamlit) :** Fatima
  * Création d'un dashboard web interactif interrogeant directement la base DuckDB (4 axes d'analyse), nettoyage à la volée des données manquantes et intégration des indicateurs de performance (KPI).

## Installation et lancement

1. **Cloner le dépôt :**
   ```bash
   git clone [https://github.com/boussalaouidapython -m venv venv
# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activpip install dbt-duckdb duckdb streamlit pandascd airbnb_analytics
dbt seed
dbt run
cd ..
streamlit run app.py
ate
d78-Fa/airbnb-analytics-platform.git](https://github.com/boussalaouidad78-Fa/airbnb-analytics-platform.git)
   
