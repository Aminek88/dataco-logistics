FROM confluentinc/cp-kafka:latest

# Passer à l'utilisateur root pour les opérations
USER root

# Installer wget si nécessaire et télécharger Kafka
RUN wget -qO- https://archive.apache.org/dist/kafka/3.7.0/kafka_2.13-3.7.0.tgz | tar -xz -C /opt && \
    mv /opt/kafka_2.13-3.7.0 /opt/kafka && \
    chown -R 1001:1001 /opt/kafka

# Ajouter les scripts Kafka au PATH
ENV PATH="/opt/kafka/bin:${PATH}"

# Revenir à l'utilisateur non-root de Confluent
USER 1001