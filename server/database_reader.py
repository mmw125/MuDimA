
def get_topics():
    return {"topics": [{"title": "Stephen Paddock, Las Vegas Suspect, Was a Gambler, a Cipher, a 'Lone Wolf'",
                       "image": "https://static01.nyt.com/images/2017/10/02/us/03Vegas-HP-slide-VRK0/"
                                "03Vegas-HP-slide-VRK0-master768.jpg", "id": "123abc"},
            {"title": "Facebook Says It Will Hire 1,000 People to Review Ads to Deter Russian Interference",
                       "image": "http://www.telegraph.co.uk/content/dam/technology/2016/05/26/84898948-facebook-tech-"
                                "xlarge_trans_NvBQzQNjv4BqFZ2mKB99NyfWHs4BvtAqLsS4XZFk3S07juafvYzyvW0.jpg",
             "id": "456dfg"}]}


def get_stories_for_topic(topic_id):
    if topic_id == "123abc":
        return ("https://www.nytimes.com/2017/10/02/us/stephen-paddock-vegas-shooter.html",
                "https://www.cbsnews.com/news/las-vegas-shooting-stephen-paddock-what-we-know-about-shooter/",
                "http://www.cnn.com/2017/10/02/us/las-vegas-attack-stephen-paddock-trnd/index.html")
    elif topic_id == "456dfg":
        return ["http://fortune.com/2017/10/02/facebook-ads-russia/",
                "https://www.rt.com/usa/405361-zuckerberg-apologizes-facebook-division/"]
    return []
