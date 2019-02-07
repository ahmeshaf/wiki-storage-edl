import unittest
from wikipedia_local import WikipediaLocal
class WikipediaLocalTests(unittest.TestCase):

    def setUp(self):
        self.wiki = WikipediaLocal()

    def test_category_members(self):
        members = self.wiki.category_members("Human_name_disambiguation_pages", limit=50)
        self.assertEqual(len(members), 50)

    def test_dis_pages(self):
        members = self.wiki.disambiguation_pages("Human_name_disambiguation_pages", limit=250)
        self.assertEqual(len(members), 250)

    def test_inlinks(self):
        title = 'Barack_Obama'
        inlinks = self.wiki.get_inlinks_by_title(title, 4582)
        self.assertEqual(len(inlinks), 4582)

    def test_outlinks(self):
        title = 'Barack_Obama'
        outlinks = self.wiki.get_outlinks_by_title(title, 100)
        self.assertEqual(len(outlinks), 100)

    def test_inlink_ids(self):
        title = 'Barack obama'
        inlinks = self.wiki.get_inlink_ids(title, 13745)
        self.assertEqual(len(inlinks), 13744)

    def test_possible_disambiguation_pages(self):
        title = "John_Smith"
        dis_pages = self.wiki.possible_disambiguation_pages(title)
        self.assertEqual(len(dis_pages), 350)

    def test_num_page_views(self):
        name = "Barack_Obama"
        id = 534366
        self.assertEqual(self.wiki.page_views(name), 18854514)
        self.assertEqual(self.wiki.page_views('', id=id), 18854514)

    def test_num_inlinks(self):
        name = "Barack_Obama"
        id = 534366
        self.assertEqual(self.wiki.inlink_count(name), 16570)
        self.assertEqual(self.wiki.inlink_count('', id), 16570)

    def test_random_pages(self):
        rows = self.wiki.random_pages(100)
        self.assertEqual(len(rows), 100)

if __name__ == "__main__":

    # run unit tests
    unittest.main()