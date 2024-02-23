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

>Aucune action requise, le code va automatiquement créé la base de données si elle n'existe pas

- Pour créer la base de données manuellement dans HBase   
```
create 'events', 'info' 
```

- Pour lister le contenu de la DB HBase   
```
hbase shell
list
```

- Pour afficher\compter le contenu de 'events'   
```
scan 'events'
count 'events'
```

- Pour vider le contenu de 'events'  
```
truncate 'events'
```




---
####Liens utiles:

- Pour voir le schema de la db  'events'  
[http://localhost:8080/events/schema](http://localhost:8080/events/schema)


- Pour de plus ample renseigneemnt sur l'API REST hBase:
[Documentation API REST hBAse](https://docs.cloudera.com/runtime/7.2.17/accessing-hbase/topics/hbase-using-the-rest-api.html)

- Présentation  PPT
[Mise en Place d'une Chaîne de Streaming avec Docker et Kafka](https://docs.google.com/presentation/d/17qMN0O-_5J6BizmE73h92diytNEkZri9/edit#slide=id.g2baa30edff1_2_0)

