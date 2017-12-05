"""A place for all of those "magic numbers" that may need to be fiddled with."""

# There must be this much keyword similarity to attach two articles together.
MIN_GROUPING_PERCENTAGE = .25

# If two groupings both have this similarity to an article, combine the groups.
MIN_COMBINE_GROUP_PERCENTAGE = .6

# Articles get removed from the database after 2 days
ARTICLE_REPLACEMENT_TIME = 2

# Number of articles to display per page on the front end
ARTICLES_PER_PAGE = 10

# Number of new articles needed before the all fit is updated.
ARTICLES_NEEDED_BEFORE_ALL_FIT_UPDATED = 200

# Number of keywords to return by default.
DEFAULT_NUM_KEYWORDS = 10

# When the user requests a grouping that does not exist in the database.
NO_SUCH_TOPIC = "There is no grouping with that id"
