# DataCo Logistics Project
Projet pour surveiller et optimiser les flux logistiques et la gestion des stocks.

## Structure
- `airflow/` : Orchestration des pipelines avec Airflow.
- `api/` : APIs REST pour logistics, predictions, reports.
- `dbt/` : Transformations des données dans Snowflake.
- `ml/` : Modèles ML pour prédire les retards.
- `streamlit/` : Dashboards interactifs.

## Prérequis
- Docker & Docker Compose
- Compte Snowflake

## Installation
1. Cloner le dépôt.
2. Configurer `.env` avec les identifiants Snowflake et Kafka.
3. Lancer les services :
   ```bash
   docker-compose up -d