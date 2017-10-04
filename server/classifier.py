import constants
import news_fetcher
import uuid


class Grouping(object):
    """Represents a set of articles that should be about the same topic."""
    def __init__(self, article):
        self._articles = [article]
        self._uuid = None

    def add_article(self, article):
        self._articles.append(article)

    def get_articles(self):
        return self._articles

    def combine_group(self, group):
        self._articles.extend(group.get_articles())

    def best_similarity(self, article):
        return max(article.keyword_similarity(group_article) for group_article in self._articles)

    def get_title(self):
        """Find the title that has the most in common with the other titles."""
        if len(self._articles) == 1:
            return self._articles[0].get_title()
        best = None
        best_similarity = 0
        for article in self._articles:
            article_set = set(article.get_title().split(' '))
            similarities = []
            for other in self._articles:
                if article != other:
                    other_set = set(other.get_title().split(' '))
                    similar = float(len(other_set.intersection(article_set)))
                    similar = 0 if similar == 0 else similar / min((len(article_set), len(other_set)))
                    similarities.append(similar)
            similarity = sum(similarities) / max(len(similarities), 1)
            if similarity >= best_similarity:
                best_similarity = similarity
                best = article
        return best.get_title()

    def get_image_url(self):
        for article in self._articles:
            if article.get_url_to_image():
                return article.get_url_to_image()
        return None

    def get_uuid(self):
        if self._uuid is None:
            self._uuid = uuid.uuid4()
        return str(self._uuid)

    def __str__(self):
        return '\n'.join([str(art) for art in self._articles])


def group_articles(article_list):
    """Group articles from the article list into Grouping objects."""
    article_list = [news_fetcher.Article(url=a) if isinstance(a, (str, unicode)) else a for a in article_list]
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
    for a in articles:
        print a
    grouped = group_articles(articles)
    for group in grouped:
        print "---------------------------------------------------"
        print group.get_title()
        for a in group.get_articles():
            print a
