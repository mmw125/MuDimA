import constants
import news_fetcher


class Grouping(object):
    """Represents a set of articles that should be about the same topic."""
    def __init__(self, article):
        self._articles = [article]

    def add_article(self, article):
        self._articles.append(article)

    def get_articles(self):
        return self._articles

    def combine_group(self, group):
        self._articles.extend(group.get_articles())

    def best_similarity(self, article):
        return max(article.keyword_similarity(group_article) for group_article in self._articles)

    def __str__(self):
        return '\n'.join([str(art) for art in self._articles])


def group_articles(article_list):
    """Group articles from the article list into Grouping objects."""
    article_list = [a if isinstance(a, news_fetcher.Article) else news_fetcher.Article(url=a) for a in article_list]
    groupings = []
    for article in article_list:
        best_grouping, best_grouping_similarity = None, 0

        # Need to make a shallow copy of list for the possibility of combining two of the items in the list.
        for grouping in groupings[:]:
            similarity = grouping.best_similarity(article)
            if similarity > best_grouping_similarity:
                # If this article has a high similarity with two separate groups, then combine the groups.
                if best_grouping_similarity > constants.MIN_COMBINE_GROUP_PERCENTAGE:
                    grouping.combine_group(best_grouping)
                    groupings.remove(best_grouping)
                best_grouping = grouping
                best_grouping_similarity = similarity

        if best_grouping is not None and best_grouping_similarity > constants.MIN_GROUPING_PERCENTAGE:
            best_grouping.add_article(article)
        else:
            groupings.append(Grouping(article))
    return groupings

if __name__ == "__main__":
    articles = news_fetcher.get_top_headlines()[:20]
    for article in articles:
        print article
    grouped = group_articles(articles)
    for group in grouped:
        print "---------------------------------------------------"
        for article in group.get_articles():
            print article
