# Wikipedia access module

Two ways to access Wikipedia data:

1. A pythonic wrapper for the Wikipedia API: https://github.com/goldsmith/Wikipedia
2. Local Wikipedia MySql database: Will need to be in University of Colorado network to use this database. 
   - mysql server address: 128.138.157.127:3306
   - username: verbs 
   - pass: verbs123
   - db_name: wiki_db
   
    Tables schema::
    
    - Page: |id|pageId|name|text|spaced_title|
    - Category: |pageId|name|
    - category_pages: |id|pages|
    - page_categories: |id|pages|
    - links: |inlink|outlink|
    - page_views: |pageId|name|views|
    - page_redirects: |id|redirects|
    
    Please follow the instructions @ https://pypi.org/project/mysqlclient/ to install MySQL for python.