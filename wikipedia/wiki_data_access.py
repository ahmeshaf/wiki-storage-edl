"""
This is a simple interface for fetching Wikipedia data. The idea is that
our code should use this as an interface for fetching data, that way we can
support multiple data sources (e.g. our own wiki database, WikiMedia API).
"""

import wikipedia as wiki
from wikipedia.wikipedia_local import WikipediaLocal

import random
random.seed(42)
# Can be wikimedia or database.
#   -wikimedia is the Wikipedia API
#   -database is our Wikipedia database
API = "wikimedia"
LOCAL = "local"

class WikiDataAccess:

    def __init__(self, fetch_source=API):
        self.fetch_source = fetch_source
        if fetch_source == LOCAL:
            self.wiki_local = WikipediaLocal()

    def fetch_category_members(self, title, limit):
        """
        Fetches the members of a given Wikipedia category.
        :param title: The title of the given category page
        :param limit: max titles to return
        :return: a list of Wikipedia page titles.
        """
        try:
            if self.fetch_source == API:
                return wiki.category_members(title, limit)
            else:
                links = self.wiki_local.disambiguation_pages(title, limit=limit)
                return [link[0] for link in links]
        except:
            print("Error while getting category members! Returning empty list.")
            return []

    def fetch_disambiguation_pages(self, disambiguation_category_title, limit):
        """
            Fetches the disambiguation pages.
            :param title: The title of the given disambiguation_category
            :param limit: max titles to return
            :return: a list of Wikipedia page titles.
            """
        try:
            if self.fetch_source == API:
                return wiki.category_members(disambiguation_category_title, limit)
            else:
                links = self.wiki_local.disambiguation_pages(disambiguation_category_title, limit=limit)
                return [link[0] for link in links]
        except:
            print("Error while getting category members! Returning empty list.")
            return []

    def fetch_disambiguation_links(self, title):
        """
        Fetches disambiguation links from a given disambiguation page.
        Will return None if the given page is not a disambiguation page.
        :param title: The title of the disambiguation page
        :return: a list of Wikipedia page titles or None
        """
        try:
            if self.fetch_source == API:
                return wiki.disambiguation_links(title)
            else:
                links = self.wiki_local.get_outlinks_by_title(title)
                return [link[0] for link in links]
        except:
            print("Error while getting disambiguation links! Returning empty list.")
            return []

    def fetch_backlinks(self, title, limit):
        """
        Fetches backlinks for a given Wikipedia page.
        :param title: the title of the Wikipedia page
        :param limit: max titles to return
        :return: a list of Wikipedia page titles.
        """
        try:
            if self.fetch_source == API:
                return wiki.backlinks(title, limit)
            else:
                links = self.wiki_local.get_inlinks_by_title(title, limit)
                return [link[0] for link in links]
        except Exception as e:
            print("Error while getting backlinks! Returning empty list. Error: %s" % e)
            return []

    def fetch_backlink_ids(self, title, limit=2147483647):
        """
        Fetches backlink ids for a given Wikipedia page.
        :param title: the title of the Wikipedia page
        :param limit: max titles to return
        :return: a list of Wikipedia page titles.
        """
        try:
            if self.fetch_source == API:
                raise Exception("Not supported by API!")
            else:
                return self.wiki_local.get_inlink_ids(title, limit)
        except Exception as e:
            print("Error while getting backlink ids! Returning empty list. Error: %s" % e)
            return []

    def fetch_outlinks(self, title, limit):
        """
        Fetches outlinks for a given Wikipedia page.
        :param title: the title of the Wikipedia page
        :return: a list of Wikipedia page titles.
        """
        try:
            if self.fetch_source == API:
                return wiki.outlinks(title, limit)
            else:
                links = self.wiki_local.get_outlinks_by_title(title, limit)
                return [link[0] for link in links]
        except Exception as e:
            print("Error while getting outlinks! Returning empty list. Error: %s" % e)
            return []

    def fetch_outlink_ids(self, title, limit=2147483647):
        """
        Fetches outlink ids for a given Wikipedia page.
        :param title: the title of the Wikipedia page
        :return: a list of Wikipedia page titles.
        """
        try:
            if self.fetch_source == API:
                raise Exception("Not supported by API!")
            else:
                links = self.wiki_local.get_outlinks_by_title(title, limit)
                return [link[1] for link in links]
        except Exception as e:
            print("Error while getting outlink ids! Returning empty list. Error: %s" % e)
            return []

    def fetch_entity_content(self, title):
        """
        Fetches the content for a given Wikipedia page.
        :param title: the title of the Wikipedia page
        :return: Returns a string containing the content.
        """
        try:
            if self.fetch_source == API:
                return wiki.html(title)
            else:
                return self.wiki_local.html(title)
        except:
            print("Error while getting entity content! Returning empty string.")
            return []

    def fetch_entity_paragraphs(self, title):
        try:
            if self.fetch_source == API:
                raise Exception("fetch_entity_paragraphs not supported in API!")
            else:
                return self.wiki_local.html_paragraphs(title)
        except Exception as e:
            print("Error while getting entity paragraphs! Returning empty string. Error: %s" % e)
            return []

    def fetch_page_views(self, title, start="2016010100", end="2016123100"):
        """
        Fetches the page view stats for a given Wikipedia page.
        :param title: the title of the Wikipedia page
        :param start:
        :param end:
        :return:
        """
        try:
            if self.fetch_source == API:
                return wiki.page_views(title, start, end)
            else:
                return self.wiki_local.page_views(title)
        except Exception as e:
            print("Error while getting page views! Returning empty string. Error: %s" % e)
            return 0

    def fetch_inlink_count(self, title):
        """
        Fetches the page view stats for a given Wikipedia page.
        :param title: the title of the Wikipedia page
        :param start:
        :param end:
        :return:
        """
        try:
            if self.fetch_source == API:
                raise Exception("fetch_entity_paragraphs not supported in API!")
            else:
                return self.wiki_local.inlink_count(title)
        except Exception as e:
            print("Error while getting inlink count! Returning empty string. Error: %s" % e)
            return 0

    def populate_random_pages(self, limit=200):
        """
        Fetch and store some page titles randomly so that it can be used to create noise
        :param limit: number
        :return: None
        """
        self.random_pages_ = self.wiki_local.random_pages(limit=limit)

    def fetch_random_pages(self, limit=1):
        """
        get some random pages from stored random pages
        :return: [(pageId, name)]
        """
        return random.choices(self.random_pages_, k=limit)

    def fetch_categories(self, title):
        """
        Fetches the members of a given Wikipedia category.
        :param title: The categories of a title
        :return: a list of categories.
        """
        try:
            categories = self.wiki_local.categories(title)
            return [category[0] for category in categories]
        except:
            print("Error while getting category members! Returning empty list.")
            return []

    def fetch_all_page_views(self):
        '''
        fetch all page views
        :return:
        '''
        try:
            all_page_views = self.wiki_local.get_all_page_views()
            return [page_view[0] for page_view in all_page_views]
        except:
            print("Error getting all page views")