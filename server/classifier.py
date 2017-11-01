"""Classifies articles together based on their keywords."""

import constants
import database_reader
import database_writer
import models


def group_articles(article_list, debug=False):
    """Group articles from the article list into Grouping objects."""
    article_list = [models.Article(url=a) if isinstance(a, (str, unicode)) else a for a in article_list]
    groupings = database_reader.get_grouped_articles()
    no_keyword_grouping = None
    for index, article in enumerate(article_list):
        if debug:
            print "Grouping", index, "out of", len(article_list)
        if not article.get_keywords():
            if no_keyword_grouping is None:
                # in_database is set to True here because we do not want a no keyword grouping in the database.
                no_keyword_grouping = models.Grouping(article, in_database=True)
            else:
                no_keyword_grouping.add_article(article)
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
    if no_keyword_grouping:
        groupings.append(no_keyword_grouping)
    return groupings
