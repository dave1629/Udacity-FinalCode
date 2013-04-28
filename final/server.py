"""
Server 

Udacity cs101 
Unit 11 (Final Version)
"""

from search import lucky_search, ordered_search
from crawler import crawl_web
from datetime import datetime
import web
import pickle
        
class About(object):        
    def GET(self):
        return "This is my udacious project!"

# adding logging will be a homework question
def log_request(q):
    try:
        log_file.write(str(datetime.now()) + ": " + q)
    except IOError, e:
        print "Logging error: " + str(e)
    except Exception, e: # note that web.application catches all exceptions processing reqs!
        print "Mysterious logging error: " + str(e)

def show_link(url):
    return "<a href=" + url + ">" + url + "</a>"

class Search(object):        
    def GET(self, query):
        response = "<html><body><h2>Search results for: " \
            + query + "</h2><p>\n"
        log_request(query)
        result = self.do_search(corpus, query)
        if not result:
            response += 'No occurences found.  Try ' + \
                '<a href="http://searchwithpeter.info/secretplans.html?q=' \
                + query + '">searchwithpeter.info</a>'
        else:
            if isinstance(result, str):
                response += result
            else:
                response += '<br>\n'.join([show_link(res)
                                           for res in result])
        return response

class LuckySearch(Search):        
    def do_search(self, corpus, query):
        return lucky_search(corpus, query)

class OrderedSearch(Search):        
    def do_search(self, corpus, query):
        return ordered_search(corpus, query)

if __name__ == '__main__':
    try:
        log_file = open('log.txt', 'w+')
    except Exception, e:
        print "Cannot open log file"

    fname = 'corpus.pkl'
    try:
        with open(fname, 'r') as fin:
            corpus = pickle.load(fin)
    except IOError, e:
        print "Cannot open web corpus: re-crawling..."
        corpus = crawl_web('http://udacity.com/cs101x/urank/index.html')

    app = web.application(('/about', 'About', '/(.*)', 'OrderedSearch'), 
                          globals())
    app.run()

