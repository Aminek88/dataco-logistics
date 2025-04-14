#!/bin/bash

# Attendre que Postgres soit prêt
until pg_isready -h postgres -p 5432 -U airflow; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
done

echo "PostgreSQL is ready, proceeding with Airflow initialization."

# Initialiser la base de données
airflow db init

# Créer l'utilisateur admin
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email amine.kon@gmail.com \
    --password admin

# Lancer webserver et scheduler en parallèle
airflow webserver & airflow scheduler