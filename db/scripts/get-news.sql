--Get news by article id
SELECT * FROM Article WHERE id = article_id;

--Get news list by topic id
SELECT * FROM Article WHERE Topic_id = topic_id;

--Get news clusters by topic id
SELECT * FROM Article WHERE Cluster_id = cluster_id;

--Get list of news list by topic id and cluster id
SELECT * FROM Article WHERE Cluster_id = cluster_id AND Topic_id = topic_id;
