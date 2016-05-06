""" A depth traversal/search of internal wiki links from a beginning article.

Observation: Links in a wiki are one-way. It is not necessary to subtract 
                source when traversing links by depth.



Naming Idea: "Depth Charge" - because it's cool. Also we are doing a depth 
                based search.
"""
import requests
import logging
import os

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Links(Base):
    """ 
    Timestamps are for internal use. Use unix epoch time.

    Wikipedia Title Limit:
    https://en.wikipedia.org/wiki/Wikipedia:Naming_conventions_(technical_restrictions)#Title_length

    256*5000=1,280,000

    """
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    page = Column(String(256))
    links = Column(String(1280000))
    timestamp = Column(Integer)


PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DB_NAME = "links.sqlite"
DB_DIR = "database"
SQLITE_DB = 'sqlite:////' + os.path.join(PROJECT_ROOT, DB_DIR, DB_NAME)

engine = create_engine(SQLITE_DB)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# note, unix epoch time as int: int(time.time())

LOG_FILENAME = "debug.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

DEPTH = 2
TRAVERSAL_SPEED_S = 0.3

TARGET_WIKI_URL = "https://en.wikipedia.org/w/api.php"

# easy to read header config section
headers = dict()
headers['user-agent'] = 'wGJF/0.0.1'

# used to track unrelated links and reduce traversals. See recursive base case.
EXHAUSTED_TITLE_DEPTHS = dict()


def endpoint_initializer(title, pllimit='5000', prop='links', action='query', _format='json'):
    """ Set up an endpoint with some defaults and an article title.
    """

    # this formatting is a little easier on the eyes for simple settings dicts.
    endpoint = dict()
    endpoint['action'] = action
    endpoint['format'] = _format
    endpoint['titles'] = title
    endpoint['prop'] = prop
    endpoint['pllimit'] = pllimit
    #endpoint['prop'] = 'revisions'
    #endpoint['rvprop'] = 'content'

    return endpoint


def get_exit_links(url, headers, endpoint):
    """ Build the request, hit the URL specified in params, return the exit_links
    """
    r = requests.get(url, headers=headers, params=endpoint)

    # munge exit links from the json response
    if r.status_code == 200:
        exit_links = list()
        entry_info = r.json()
        for k, v in entry_info['query']['pages'].iteritems():
            if len(entry_info['query']['pages'].keys()) > 1:
                logging.debug("Why was more than one page returned in this query?")
            if 'links' in v:
                for link in v['links']:
                    if link['ns'] == 0:
                        exit_links.append(link['title'])

    else: 
        logging.debug("Request failed at: {}, error {}.".format(url, r.status_code))

    if len(exit_links) > 5000:
        logging.debug("More than 5000 titles at: {}, a longer handling script should be created.".format(url))

    return exit_links


def collect_routes(depth_counter, next_title, title_route=tuple()):
    """ Recursively collect each route back to the source material.

    This recursive function traverses deep links in wikipedia and
        searches for links back to the source material.
    """
    title_route += (next_title,)

    print("Traversing Route: {}".format(title_route))

    import time; time.sleep(TRAVERSAL_SPEED_S)

    endpoint = endpoint_initializer(next_title)

    exit_links = get_exit_links(TARGET_WIKI_URL, headers, endpoint)

    # record routes that return to the source title.
    if TARGET_TITLE in exit_links:
        print(depth_counter, title_route)
        logging.debug("Return route found at depth {}: {}".format(depth_counter, title_route))

    if depth_counter > 0:

        for title in exit_links:
            # keep digging unless we hit the source title.

            # depth will never be < 1 here.
            # the depth_counter check skips queries if depth_counter or 
            # shallower was already traversed according to EXHAUSTED_TITLE_DEPTHS.
            if depth_counter > EXHAUSTED_TITLE_DEPTHS.get(title, -1) and title != title_route[0]:
                collect_routes((depth_counter-1), title, title_route)

    else:
        # base case
        pass

    """
    One way we can prevent repeat traversals is to add to the global 
    exhaustion list only from the nearest nodes to the source node.

    We could actually do an exhaustion dictionary. If an item is exhausted we 
    record the depth it is exhausted at.

    If it is tested at a higher depth we then refer to the dictionary and 
    discover we should test it some more.
    """
    # add depth counters when traversing back up the recursion chain
    if next_title in EXHAUSTED_TITLE_DEPTHS:
        if EXHAUSTED_TITLE_DEPTHS[next_title] < depth_counter:
            EXHAUSTED_TITLE_DEPTHS[next_title] = depth_counter
    else:
        EXHAUSTED_TITLE_DEPTHS[next_title] = depth_counter

    return


if __name__ == "__main__":
    """
    What kind of result do we want?

    A list of tuples with the title and the depth would be cool.
    However, we are supposed to return the whole route.
    So it would be more like a list of titles, starting with the source
    and ending with the title that references the source.

    This is a good place for recursion.
    Spawn a new controller for each item in the exit_links list.

    """
    # use care, underscores in the url need to be spaces in the title for the comparison to work.
    ROOT_TITLE = "Python (programming language)"
    TARGET_TITLE = ROOT_TITLE

    collect_routes(DEPTH, ROOT_TITLE)

