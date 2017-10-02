import MySQLdb
import sys
import dbconstants as dbconst


def db_connect():
    connection = MySQLdb.connect(host=dbconst.HOST, user=dbconst.USER, passwd=dbconst.PASSWD, db=dbconst.DB)
    cursor = connection.cursor()
    return connection, cursor


def get_topics():
    connection, cursor = db_connect()
    try:
        cursor.execute("SELECT * FROM Topic;")

        return cursor.fetchall

    except:
        print "Couldn't get topics"

    finally:
        cursor.close()
        connection.close()
    '''
    return {"123abc": {"title": "Trump loses game of Tic-Tac-Toe",
                       "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/"
                                "Turnip_2622027.jpg/1200px-Turnip_2622027.jpg"},
            "456dfg": {"title": "4 great exercises for asthma",
                       "image": "https://i.pinimg.com/736x/d5/69/12/d569124e89a11274f7144a21ebc9c18f"
                                "--funny-guys-funny-memes.jpg"}}
    '''


def get_stories_for_topic(topic_id):
    try:
        connection, cursor = db_connect()
        cursor.execute(query)
        cursor.execute("SELECT * FROM Article WHERE Topic_id = %s;", topic_id)

        return cursor.fetchall

    except:
        print "Couldn't get stories from topic"

    finally:
        cursor.close()
        connection.close()

    '''
    if topic_id == "123abc":
        return "example.com", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    elif topic_id == "456dfg":
        return ("http://inhealth.cnn.com/taking-control-of-your-asthma/4-great-exercises-for-asthma?did=t1_rss12",
                "example.com")
    return []
    '''
