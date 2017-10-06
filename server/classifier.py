import constants
import database_utils
import news_fetcher


def group_articles(article_list):
    """Group articles from the article list into Grouping objects."""
    article_list = [database_utils.Article(url=a) if isinstance(a, (str, unicode)) else a for a in article_list]
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
            groupings.append(database_utils.Grouping(article))
    return groupings

if __name__ == "__main__":  # pragma: no cover
    articles = news_fetcher.get_top_headlines()[:20]
    for a in articles:
        print a
    grouped = group_articles(articles)
    for group in grouped:
        print "---------------------------------------------------"
        print group.get_title()
        for a in group.get_articles():
            print a
