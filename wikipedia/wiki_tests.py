import unittest
from wikipedia.wikipedia_local import WikipediaLocal
from wikipedia.wiki_data_access import WikiDataAccess
import wikipedia.wikipedia as wiki

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

class WikiDataAccessLocalTests(unittest.TestCase):

    """
    Unit tests for wiki_data_access.py
    """

    def setUp(self):
        self.dao = WikiDataAccess("local")

    def test_backlinks(self):
        links = self.dao.fetch_backlinks("Paris", 15)
        self.assertEqual(len(links), len(set(links)))
        self.assertEqual(len(links), 15)

        # Check the exact links
        self.assertEqual(links[0], "Bud_Moore_(NASCAR_owner)")
        self.assertEqual(links[1], "Elvis_Pompilio")
        self.assertEqual(links[2], "Birmingham_Surrealists")
        self.assertEqual(links[3], "List_of_Star_Trek_planets_(C–F)")
        self.assertEqual(links[4], "Pascal_Pia")
        self.assertEqual(links[5], "Bernadette_Allen")
        self.assertEqual(links[6], "Louis_Dumoulin")
        self.assertEqual(links[7], "Patrick_Boyle,_10th_Earl_of_Glasgow")
        self.assertEqual(links[8], "Carolina_Gynning")
        self.assertEqual(links[9], "Zora_sourit")
        self.assertEqual(links[10], "International_Conference_to_Review_the_Global_Vision_of_the_Holocaust")
        self.assertEqual(links[11], "Antonio_Fontanesi")
        self.assertEqual(links[12], "Evelyn_Hoey")
        self.assertEqual(links[13], "Martin_W._Littleton")
        self.assertEqual(links[14], "Maurice_Martenot")

    def test_outlinks(self):
        links = self.dao.fetch_outlinks("Paris", 15)
        self.assertEqual(len(links), len(set(links)))
        self.assertEqual(len(links), 15)

        # Check the exact links
        self.assertEqual(links[0], "Capital_city")
        self.assertEqual(links[1], "List_of_communes_in_France_with_over_20,000_inhabitants")
        self.assertEqual(links[2], "France")
        self.assertEqual(links[3], "Gross_domestic_product")
        self.assertEqual(links[4], "List_of_cities_by_GDP")
        self.assertEqual(links[5], "Economist_Intelligence_Unit")
        self.assertEqual(links[6], "Singapore")
        self.assertEqual(links[7], "Zurich")
        self.assertEqual(links[8], "Hong_Kong")
        self.assertEqual(links[9], "Oslo")
        self.assertEqual(links[10], "Geneva")
        self.assertEqual(links[11], "Île_de_la_Cité")
        self.assertEqual(links[12], "Seine")
        self.assertEqual(links[13], "Rive_Gauche")
        self.assertEqual(links[14], "Rive_Droite")

    def test_categorymembers(self):
        category_members = self.dao.fetch_category_members("Human_name_disambiguation_pages", 10)
        self.assertEqual(len(category_members), 10)

        # # Check some members
        # self.assertEqual(category_members[0], "Albert_I")
        # self.assertEqual(category_members[1], "Albert_II")
        # self.assertEqual(category_members[2], "Albert_III")

        # Fetch them all
        category_members = self.dao.fetch_category_members("Human_name_disambiguation_pages", 100)
        self.assertEqual(len(category_members), 100)

        # # Check some members
        # self.assertEqual(category_members[0], "Albert_I")
        # self.assertEqual(category_members[1], "Albert_II")
        # self.assertEqual(category_members[2], "Albert_III")

    def test_disambiguation_links(self):

        # Test Mohammad_Aamer
        links = self.dao.fetch_disambiguation_links("Mohammad_Aamer")
        self.assertEqual(len(links), 6)
        self.assertEqual(links[0], "Mohammad_Aamer_(cricketer,_born_1965)")
        self.assertEqual(links[1], "Mohammad_Aamer_(cricketer,_born_1979)")
        self.assertEqual(links[2], "Mohammad_Aamer_(cricketer,_born_1993)")
        self.assertEqual(links[3], "Mohammad_Aamer_(cricketer,_born_1995)")
        self.assertEqual(links[4], "Mohammad_Aamer_(Lahore_cricketer)")
        self.assertEqual(links[5], "Mohammad_Amir")

        # Test Thomas_a_Beckett_(disambiguation)
        links = self.dao.fetch_disambiguation_links("Thomas_a_Beckett_(disambiguation)")
        self.assertEqual(len(links), 4)
        self.assertEqual(links[0], "Thomas_à_Beckett")
        self.assertEqual(links[1], "Thomas_Becket")
        self.assertEqual(links[2], "Thomas_Turner_à_Beckett")
        self.assertEqual(links[3], "Thomas_A'Becket_(composer)")

        # Test Héctor_Acosta
        links = self.dao.fetch_disambiguation_links("Héctor_Acosta")
        self.assertEqual(len(links), 3)
        self.assertEqual(links[0], "Héctor_Acosta_(cyclist)")
        self.assertEqual(links[1], "Héctor_Acosta_(footballer)")
        self.assertEqual(links[2], "Héctor_Acosta_(singer)")

        # Test David_Abrahams
        links = self.dao.fetch_disambiguation_links("David_Abrahams")
        self.assertEqual(len(links), 4)
        self.assertEqual(links[0], "David_Abrahams_(businessman)")
        self.assertEqual(links[1], "David_Abrahams_(computer_programmer)")
        self.assertEqual(links[2], "David_Abrahams_(mathematician)")
        self.assertEqual(links[3], "David_Abraham_(disambiguation)")

    def test_disambiguation_links_bugs(self):

        # If a page does not exist, then just don't return links.
        links = self.dao.fetch_disambiguation_links("inary earch lgorithm")
        self.assertEqual(len(links), 0)

    def test_entity_content(self):

        # Test Mohammad_Aamer_(cricketer,_born_1995)
        entity_content = self.dao.fetch_entity_content("Mohammad Aamer (cricketer, born 1965)")
        self.assertIn("Mohammad Aamer (born 9 March 1965) is a former", entity_content)

class WikiDataAccessAPITests(unittest.TestCase):

    """
    Unit tests for wiki_data_access.py
    """

    def setUp(self):
        self.dao = WikiDataAccess()

    def test_backlinks(self):
        links = self.dao.fetch_backlinks("Paris", 15)
        self.assertEqual(len(links), len(set(links)))
        self.assertEqual(len(links), 15)

    def test_outlinks(self):
        links = self.dao.fetch_outlinks("Paris", 15)
        all_links = (wiki.page("Paris")).links
        self.assertEqual(len(links), len(set(links)))
        for link in links:
            self.assertIn(link, all_links)
        self.assertEqual(len(links), 15)

    def test_categorymembers(self):
        category_members = self.dao.fetch_category_members("Human_name_disambiguation_pages", 10)
        self.assertEqual(len(category_members), 10)

    def test_disambiguation_links(self):

        # Test Mohammad_Aamer
        links = self.dao.fetch_disambiguation_links("Mohammad_Aamer")
        self.assertEqual(len(links), 6)

        # Test Thomas_a_Beckett_(disambiguation)
        links = self.dao.fetch_disambiguation_links("Thomas_a_Beckett_(disambiguation)")
        self.assertEqual(len(links), 3)

        # Test Héctor_Acosta
        links = self.dao.fetch_disambiguation_links("Héctor_Acosta")
        self.assertEqual(len(links), 3)

        # Test David_Abrahams
        links = self.dao.fetch_disambiguation_links("David_Abrahams")
        self.assertEqual(len(links), 4)

    def test_disambiguation_links_bugs(self):

        # If a page does not exist, then just don't return links.
        links = self.dao.fetch_disambiguation_links("inary earch lgorithm")
        self.assertEqual(len(links), 0)

    def test_entity_content(self):

        # Test Mohammad_Aamer_(cricketer,_born_1995)
        entity_content = self.dao.fetch_entity_content("Mohammad Aamer (cricketer, born 1965)")
        self.assertIn("<b>Mohammad Aamer</b> (born 9 March 1965) is a former", entity_content)

    def test_page_view_stats(self):
        title = "Barack Obama"
        start = "2016010100"
        end = "2016123100"
        page_stats = self.dao.fetch_page_views(title, start, end)
        self.assertGreaterEqual(page_stats, 16000000)


if __name__ == "__main__":

    # run unit tests
    unittest.main()