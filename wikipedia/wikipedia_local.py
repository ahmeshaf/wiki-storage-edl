# -*- coding: utf-8 -*-

# =============================================================================
#  Version: 0.1 (March 4, 2017)
#  Author: Rehan Ahmed (shah7567@colorado.edu), University of Colorado, Boulder
#
#  Contributors:
#   Alex Killian (alki3764@colorado.edu )
#   Dhanendra Soni (dhso4050@colorado.edu)
#
# =============================================================================
#  Copyright (c) 2018. Rehan Ahmed (shah7567@colorado.edu).g
# =============================================================================
#
#  This is a free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License, version 3,
#  as published by the Free Software Foundation.
#
#  This is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License at <http://www.gnu.org/licenses/> for more details.
#
# =============================================================================

"""
A set of queries to be able to access the local wikipedia database.

The table schemas in the database::

Page: |id|pageId|name|text|spaced_title|
Category: |pageId|name|
category_pages: |id|pages|
page_categories: |id|pages|
page_inlinks: |id|inLinks|
page_outlinks: |id|outLinks|
"""

import MySQLdb
from WikiExtractor import Extractor, normalizeTitle
import re
import random
random.seed(42)
CONSTANT_START = 58860234
class WikipediaLocal:
    """
    This class holds the sql querying methods used by our wikifier.
    """
    ALL_DISAMB_PAGE_ID = 19205681

    def __init__(self):
        self.db = MySQLdb.connect(host="128.138.157.127",  # your host
                     user="verbs",  # username
                     passwd="verbs123",  # password
                     db="wiki_db", charset='utf8', use_unicode=True)  # name of the database

    def html(self, title=None, id=None):
        """
        Get the wiki page in html format
        :param title: string
        :param id: int
        :return: html string
        """
        wiki_paras = self.html_paragraphs(title, id)
        return ''.join(wiki_paras)

    def html_paragraphs(self, title=None, id=None):
        """
        Get wiki page as a list of html paras
        :param title: string
        :param id: int
        :return: [string]
        """
        if id == None:
            id = self.get_page_id(title)
        if id == None:
            raise Exception("Invalid Title")
        query = "select text from Page where pageId = {}".format(id)
        row = self.fetch_one(query)
        if row == None:
            raise Exception("Invalid Id")
        text = row[0]
        wiki_paras = ['<p>{}</p>'.format(t) for t in wiki2text(id, title, text)[1:] if t.strip() != '']
        return wiki_paras

    def __get_redirect_id(self, title):
        """
        Expects an already clean title! This is private. It's called as a backup
        in get_page_id.
        :param title: string
        :return:
        """
        query = '''select id from page_redirects where redirects like "%s";''' % title
        row = self.fetch_one(query)
        if row == None: raise Exception("Invalid Title: %s" % title)
        return row[0]

    def get_page_id(self, title):
        """
        Get page id of a wiki page with its title
        :param title: string
        :return: int
        """
        normalized_title = clean_title(title)
        query = '''select id from Page where name like "%s";''' % normalized_title
        row = self.fetch_one(query)
        if row == None: return self.__get_redirect_id(title)
        return row[0]

    def page(self, title):
        """
        get the page text stored in Page table
        :param title: string
        :return: string
        """
        title = clean_title(title)
        query = "select id, name, text from Page where name like {} limit 1;".format(title)
        cur = self.db.cursor()
        cur.execute(query)
        row = cur.fetchone()
        cur.close()
        return row[2]

    #def get_inlinks_by_id(self, id, limit=500):
    #    query = "select Page.name, page_inlinks.inLinks from page_inlinks \
    #            inner join Page on inLinks = pageId where page_inlinks.id = {} \
    #            limit {};".format(id, limit)
    #    row = self.fetch_all(query)
    #    return list(row)

    def get_inlinks_by_title(self, title, limit=500):
        """
        get the inlinks of a wiki title
        :param title: string
        :param limit: int
        :return: [string]
        """
        title = clean_title(title)
        query = '''select distinct Page.name, links.inlink from links
                inner join Page on inlink = pageId where outlink like "%s"
                limit %s;''' % (title, limit)
        row = self.fetch_all(query)
        if row == None: raise Exception("No found inlinks!")
        result = list(row)
        if len(result) == 0: raise Exception("No found inlinks!")
        return result

    def get_inlink_ids(self, title, limit=500):
        """
        get inlink ids of a wiki title
        :param title: string
        :param limit: int
        :return: [int]
        """
        title = clean_title(title)
        query = '''select distinct inlink from links where outlink like "%s" limit %s;''' % (title, limit)
        row = self.fetch_all(query)
        if row == None: raise Exception("No found inlinks!")
        result = list([r[0] for r in row])
        if len(result) == 0: raise Exception("No found inlinks!")
        return result

    def get_outlinks_by_id(self, id, limit=500):
        """
        get outlinks of a wiki page by its id
        :param id: int
        :param limit: int
        :return: [string]
        """
        query = '''select distinct outlink from links where inlink = %s limit %s;''' % (id, limit)
        row = self.fetch_all(query)
        return list(row)

    def get_outlinks_by_title(self, title, limit=500):
        """
        get outlinks of a wiki page by its title
        :param title: string
        :param limit: int
        :return: [string]
        """
        query = '''select outlink 
        from (Select pageId from Page where name like "%s") a,
        links where inlink = pageId limit %d;''' %(title, limit)
        row = self.fetch_all(query)
        return row

    def category_members(self, category_name, limit=500):
        '''
        get category members from the database for a category name
        :param category_name:
        :param limit: number of category members
        :return: [(title, pageId)]
        '''
        assert limit <= 59464 and limit > 0, "limit should be between 0 and 59464"
        category_name = clean_title(category_name)
        query_category_id = "select pageId from Category where name like '{}'".format(category_name)
        row = self.fetch_one(query_category_id)
        if row == None:
            raise Exception("Invalid Category name")
        category_id = str(row[0])
        query_category_page_members = '''
            select name, pageId from
                (select pages from category_pages where id = %s order by rand() limit %d) a,
                Page where pages = pageId;
        ''' % (category_id, limit)
        category_members = self.fetch_all(query_category_page_members)
        return category_members

    def disambiguation_pages(self, dismabiguation_category, max_cat_pages=4000, min_count=7, max_count=20, limit=250):
        """
        Get the disambiguation pages within a disambiguation category
        :param dismabiguation_category: string
        :param max_cat_pages: int
        :param min_count: int
        :param max_count: int
        :param limit: int
        :return: [(title, id, out_links_count)]
        """
        dismabiguation_category = clean_title(dismabiguation_category)
        query_category_id = "select pageId from Category where name like '{}'".format(dismabiguation_category)
        row = self.fetch_one(query_category_id)
        if row == None:
            raise Exception("Invalid Category name")
        category_id = str(row[0])
        query_dis_pages = '''
            select c.name, c.pageId, c.out_count from (
                select b.name, b.pageId, count(b.pageId) as out_count from (
                    select name, pageId from (
                        select * from category_pages where id = %s order by rand() limit %d) a,
                        Page where pages = pageId
                    ) b, links where b.pageId = inlink
                    group by b.name, b.pageId
                ) c where c.out_count > %d and c.out_count < %d
                order by c.out_count desc
                limit %d;
        ''' % (category_id, max_cat_pages, min_count, max_count, limit)
        category_members = self.fetch_all(query_dis_pages)
        return category_members

    def categories(self, title):
        '''
        Get categories a title is part of
        :param title:
        :return: [categories]
        '''
        title = clean_title(title)
        query = '''select category_pages.id 
                   from (select Page.id from Page where name like "%s")a, category_pages
                   where a.id = category_pages.pages;''' % (title)
        cats = self.fetch_all(query)
        return list(cats)

    def possible_disambiguation_pages(self, title):
        '''
        Get the possible titles from the database that might be the page for given title.
        Look from the disambiguation pages and try to find all
        :param title: string
        :return: [disamguation_page_id, full_text_score, page_name, num_inlinks, num_views]
        '''
        # spaced_title = normalizeTitle(title)
        spaced_title = re.sub('_', " ", title).strip()
        spaced_title_boolean = " ".join(['+{}'.format(w.strip()) for w in spaced_title.split()])
        query = '''
        select distinct c.dis_page, c.score, c.outlink, c.num_inlinks, views from
            (select * from 
                (select * from  
                    (select pages, Page.name as dis_page, match(spaced_title) against ("%s") as score from 
                        category_pages, Page where category_pages.id = 19205681 and 
                        match(spaced_title) against ("%s" in boolean mode) and 
                        pageId = pages
                    ) a, links where a.pages = inlink
                ) b, inlink_count where b.outlink = inlink_count.name) c, page_views
                where c.outlink = page_views.name order by views desc;
        ''' %(spaced_title, spaced_title_boolean)
        return [q[2].lower() for q in self.fetch_all(query)]


    def possible_disambiguation_pages_simple(self, title):
        """
        get the possible disambiguation page just by using MySql Full Text indexing
        :param title: string
        :return: [(title, match_score)]
        """
        spaced_title = normalizeTitle(title)
        spaced_title_boolean = " ".join(['+{}'.format(w.strip()) for w in spaced_title.split()])
        query = '''
                select name, match(spaced_title) against ("%s") as score from Page
                where match(spaced_title) against ("%s" in boolean mode) 
                order by score desc limit 15;
                ''' % (spaced_title, spaced_title_boolean)
        return [q[0].lower() for q in self.fetch_all(query)]
        # return self.fetch_all(query)

    def page_views(self, title, id=None):
        '''
        Get the page views for a title
        :param title: string
        :param id: int
        :return: int
        '''
        title = clean_title(title)
        if id == None:
            query = '''select views from page_views where name like "%s"; ''' % (title)
        else:
            query = '''select views from page_views where pageId = %d''' % (id)
        return self.fetch_one(query)[0]

    def get_all_page_views(self):
        '''
        Get all the page views
        :return:[int]
        '''
        query = '''select views from page_views'''
        return self.fetch_all(query)

    def inlink_count(self, title, id=None):
        '''
        Get the inlink counts of a title for popularity measure
        :param title: string
        :param id: int
        :return: int
        '''
        title = clean_title(title)
        if id == None:
            query = '''select num_inlinks from inlink_count where name like "%s"; ''' % (title)
        else:
            query = '''select num_inlinks from (select name from Page where id = "%d") a, 
                       inlink_count where a.name = inlink_count.name''' % (id)
        return self.fetch_one(query)[0]

    def fetch_one(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        return row

    def fetch_all(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_page_id_and_title(self, limit=0):
        query = "select id, name from Page limit {}".format(limit)
        row = self.fetch_all(query)
        return row

    # def select_pages(self, start_index, end_index):
    def random_pages(self, limit):
        '''
        Query for random pages using index column
        :param limit: int
        :return: [(pageId, title)]
        '''
        rand_index = CONSTANT_START + random.randint(0, 4000000)
        end_index = rand_index + limit
        query = "select pageId, name from Page where `index` > %d and `index` <= %d;" %(rand_index, end_index)
        return self.fetch_all(query)


def try_queries():
    db = MySQLdb.connect(host="128.138.157.127",  # your host
                         user="verbs",  # username
                         passwd="verbs123",  # password
                         db="wiki_db", charset='utf8', use_unicode=True)  # name of the database
    query = "select * from links where inlink=6959948;"
    cur = db.cursor()
    cur.execute(query)
    row = cur.fetchall()
    pass



def wiki2text(id, title, text):
    extractor = Extractor(id, -1, title, text)
    t = extractor.extract(1)
    return t

def clean_title(title):
    '''
    Makes sure the title is ready to be injected into a query
    '''
    normalized_title = re.sub('\s', '_', title.strip())
    return re.sub('"', '""', normalized_title)

if __name__=='__main__':
    # Create a Cursor object to execute queries.
    wiki = WikipediaLocal()
    # print(wiki.html('"Anarchism"'))
    # print(wiki.html('"_obama"', 38878700))
    # print(wiki.page('"Anarchism"'))
    # print the first and second columns
    # print(wiki.get_inlinks_by_id('"600744"'))
    print(wiki.get_inlinks_by_title('Anarchism'))
    # print(wiki.get_outlinks_by_id('"600744"'))
    # print(wiki.get_outlinks_by_title('"Anarchism"'))
    #print(wiki.category_members("Human_name_disambiguation_pages"))
    #print(wiki.fetch_one("select name from Page where id = 154943;"))
    #print(wiki._WikipediaLocal__get_redirect_id("Otto_the_Child"))
    #print(wiki._WikipediaLocal__get_redirect_id("Brandenburg_an_der_Havel"))
    #print(wiki._WikipediaLocal__get_redirect_id("Albert_the_Bear"))
    # print("Num inlinks: %s" % len(wiki.get_inlink_ids("Otto_the_Child")))
    # print("Num inlinks: %s" % len(wiki.get_inlink_ids("Brandenburg_an_der_Havel")))
    # print("Num inlinks: %s" % len(wiki.get_inlink_ids("Albert_the_Bear")))
    # print("Num disambiguations: %d" %(len(wiki.possible_disambiguation_pages("John_Smith"))))
    # pass
    # with open('entity_names.txt') as ef:
    #     names = [line.strip().lower() for line in ef.readlines()]
    # n = 500
    # ds = [set(wiki.possible_disambiguation_pages_simple(name)) for name in names[:n]]
    # predicts = [name in d for name,d in zip(names[:n],ds)]
    # print(sum(predicts))
    # pass