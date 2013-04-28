###
### crawler.py
###
###

from webcorpus import WebCorpus
from getpage import get_page
from bs4 import BeautifulSoup

def get_all_links(page):
    soup = BeautifulSoup(page)
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = set([seed])
    crawled = []
    wcorpus = WebCorpus()
    while tocrawl: 
        url = tocrawl.pop() # changed page to url - clearer name
        if url not in crawled:
            content = get_page(url)
            outlinks = get_all_links(content)
            for outlink in outlinks:
                wcorpus.add_link(url, outlink) 
            for word in content.split():
                wcorpus.add_word_occurrence(url, word)
            tocrawl.update(outlinks)
            crawled.append(url)
    return wcorpus

if __name__ == '__main__':
    import pickle

    seed = 'http://udacity.com/cs101x/urank/index.html'
    corpus = crawl_web(seed)
    corpus.page_rank(seed)  # so ranks are computed and stored in file
    # write corpus to file
    fname = 'corpus.pkl'
    try:
        with open(fname, 'w') as fout:
            pickle.dump(corpus, fout)
            print "Succesfully wrote corpus to " + fname
    except IOError, e:
        print "Cannot write out corpus: " + str(e)
