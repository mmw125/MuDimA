"""A place for all of those "magic numbers" that may need to be fiddled with."""

# There must be this much keyword similarity to attach two articles together.
MIN_GROUPING_PERCENTAGE = .25

# If two groupings both have this similarity to an article, combine the groups.
MIN_COMBINE_GROUP_PERCENTAGE = .6

# Articles get removed from the database after 2 days
ARTICLE_REPLACEMENT_TIME = 2

# Number of articles to display per page on the front end
ARTICLES_PER_PAGE = 10
