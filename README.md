
[![Build Status](https://travis-ci.org/mmw125/MuDimA.svg?branch=master)](https://travis-ci.org/mmw125/MuDimA)
[![Coverage Status](https://coveralls.io/repos/github/mmw125/MuDimA/badge.svg?branch=master)](https://coveralls.io/github/mmw125/MuDimA?branch=master)

Uses [NewsAPI.org](http://beta.newsapi.org)

# Abstract

News today is easy to access with the existence of the world wide web. As the cost of storing data continues to drop, the amount of information that is added to the internet continues to increase. This makes the publishing of news articles, online, easier than ever. However, even though news information is easier to access or add to the internet doesn’t mean it is the most accurate. An author’s bias on a topic may describe the current events in a way that may mislead the reader or only show one side of the story. This can be done by an author’s selection of words in describing the news topic. We created MuDimA to solve this issue that exists, even among top news providers such as CNN, Fox News, etc. 

The purpose of our app is to gather news articles from several providers and group them into appropriate topics based off similarities between each article. We then display each topic to the user in an XY graph that shows articles about the topic as dots and how closely they relate to each other. The app does this by first scraping the internet on the server side through an API. The server then parses through the words in each article and compares them to each other for keywords that are similar. If a certain threshold is passed of similar keywords then those articles form a grouping that represents the topic. They are then stored into a database that can be requested by a client to view on their browser. The server would be constantly scraping and grouping news articles to display news that is up to date for the user. Other features that are implemented or are being implemented are searching capabilities, popular keywords, popularity for each article and sorting/filtering of topics and articles. 
