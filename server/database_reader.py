
def get_topics():
    return {"topics": [{"title": "Trump loses game of Tic-Tac-Toe",
                       "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/"
                                "Turnip_2622027.jpg/1200px-Turnip_2622027.jpg", "id": "123abc"},
            {"title": "4 great exercises for asthma",
                       "image": "https://i.pinimg.com/736x/d5/69/12/d569124e89a11274f7144a21ebc9c18f"
                                "--funny-guys-funny-memes.jpg", "id": "456dfg"}]}


def get_stories_for_topic(topic_id):
    if topic_id == "123abc":
        return ["example.com", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    elif topic_id == "456dfg":
        return ["http://inhealth.cnn.com/taking-control-of-your-asthma/4-great-exercises-for-asthma?did=t1_rss12",
                "example.com"]
    return []
