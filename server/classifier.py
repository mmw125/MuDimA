"""Classifies articles together based on their keywords."""

import constants
import database_writer
import models
import news_fetcher


def group_articles(article_list):
    """Group articles from the article list into Grouping objects."""
    article_list = [models.Article(url=a) if isinstance(a, (str, unicode)) else a for a in article_list]
    groupings = []
    for article in article_list:
        if not article.get_keywords():
            continue  # Skip the article if the keywords cannot be gotten from it.
        best_grouping, best_grouping_similarity = None, 0

        # Need to make a shallow copy of list for the possibility of combining two of the items in the list.
        for grouping in groupings[:]:
            similarity = grouping.best_similarity(article)
            if similarity > best_grouping_similarity:
                # If this article has a high similarity with two separate groups, then combine the groups.
                if best_grouping_similarity > constants.MIN_COMBINE_GROUP_PERCENTAGE:
                    if best_grouping.in_database():
                        if grouping.in_database():
                            database_writer.remove_grouping_from_database(grouping)
                        best_grouping.combine_group(grouping)
                        groupings.remove(grouping)
                    else:
                        grouping.combine_group(best_grouping)
                        groupings.remove(best_grouping)
                best_grouping = grouping
                best_grouping_similarity = similarity
        if best_grouping is not None and best_grouping_similarity > constants.MIN_GROUPING_PERCENTAGE:
            best_grouping.add_article(article)
        else:
            groupings.append(models.Grouping(article))
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
