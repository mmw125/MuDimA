--Insert Article into topic
INSERT INTO Article (name, link, summary, actualDate, Cluster_id, Topic_id)
VALUES (article.name, article.link, article.summary, article.date, article.cluster, article.topic);

--Insert Topic
INSERT INTO Topic (name)
VALUES (topic.name);

--Insert Cluster
INSERT INTO Cluster (name)
VALUES (cluster.name);
