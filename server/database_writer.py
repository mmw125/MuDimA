import dbconstants as dbconst


def db_connect():
    connection = MySQLdb.connect(host=dbconst.HOST, user=dbconst.USER, passwd=dbconst.PASSWD, db=dbconst.DB)
    cursor = connection.cursor()
    return connection, cursor


def write_topics_to_database(topic_list):
    try:
        connection, cursor = db_connect()

        cursor.executemany(
                """INSERT INTO Article (name, link, summary, actualDate, Cluster_id, Topic_id)
                VALUES (%s, %s, %s, %s, NULL, %s); """, topic_list)
        conection.commit()

    except:
        print "Didn't add news to topic"

    finally:
        cursor.close()
        connection.close()
