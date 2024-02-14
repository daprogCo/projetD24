

Commandes:
docker-compose -f docker-compose.yml up -d

-- Pour valider que la communication est ok: kafka-console-consumer.sh --topic sensordatainputfrancois --from-beginning --bootstrap-server localhost:9092 
