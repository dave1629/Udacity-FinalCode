"""
WebCorpus module for defining WebCorpus class.

Udacity cs101 Unit 9 (version 5 - end of PS9)
"""

import graph

class WebCorpus(object):
    """
    Represents the result of a web crawl.
    """

    def __init__(self):
        self._index = {}
        self._graph = graph.Graph()
        self._ranks = None 

    def add_word_occurrence(self, url, keyword):
        """
        Adds an occurrence of word on url to the corpus.
        """
        if not self._graph.has_node(url):
            self._graph.add_node(url)

        if keyword in self._index:
            self._index[keyword].append(url)
        else:
            self._index[keyword] = [url]

    def add_link(self, source, sink):
        """
        If source is not a node in the corpus, adds source as a new node.
        If sink is not a node in the corpus, adds sink as a new node.
        Adds a link from source to sink to the corpus.
        """
        if not self._graph.has_node(source):
            self._graph.add_node(source)

        if not self._graph.has_node(sink):
            self._graph.add_node(sink)

        self._graph.add_edge(source, sink)
        self._ranks = None # invalidate ranks after each graph modification
    
    def _compute_ranks(self, damping = 0.8, numloops = 10):
        """
        Compute page ranks for the input web index.  
        """
        self._ranks = {}
        nodes = self._graph.get_nodes()
        npages = len(nodes)
        for url in nodes:
            self._ranks[url] = 1.0 / npages    

        for _ in range(0, numloops):
            newranks = {}
            for page in nodes:
                newrank = (1 - damping) / npages
                outlinks = self._graph.get_outlinks(page)
                for page in outlinks:
                    newrank += damping * (self._ranks[page] / len(outlinks))
                    newranks[page] = newrank
            self._ranks = newranks

    def lookup(self, keyword):
        """Return a list of the URLs where keyword appears."""
        if keyword in self._index:
            return self._index[keyword]
        else:
            return None

    def page_rank(self, url):
        """Return the page rank of the url."""
        if not self._ranks:
            self._compute_ranks()
        if url not in self._ranks:
            return 0.0
        return self._ranks[url]
