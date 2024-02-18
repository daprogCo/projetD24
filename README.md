**Collège de Bois de Boulogne**

**420-D04-BB**

**TP – Pratique containers Dockers/Kafka dans la mise en place d'une chaine de streaming**

**Contexte : Équipe de 3 au maximum**

**OBJECTIF**

- Utiliser Docker et les containers dockers
- Utiliser un framework de traitement comme spark streaming (installation de l'outil seulement)
- Utiliser un framework d'ingestion de données 





---
####Commandes:

```
docker-compose -f docker-compose.yml up -d
```
-- Pour valider que la communication est ok: 
```
kafka-console-consumer.sh --topic sensordatainputfrancois --from-beginning --bootstrap-server localhost:9092 
```



#####HBASE:

Aucune action requise, le code va automatiquement créé la base de données si elle n'existe pas

- Pour créer la base de données manuellement dans HBase   
```
create 'events', 'info' 
```

- Pour lister le contenu de la DB HBase   
```
hbase shell
```
