## Wikipedia Generalized Jesus Finder (wGJF)

A generalized tool to find references to an article by depth-searching internal wikipedia links.

Currently the search only finds references to the originating article, unless the TARGET_TITLE is altered.

Named after ["5 clicks to Jesus"](http://www.urbandictionary.com/define.php?term=5%20Clicks%20To%20Jesus).


### What the heck is this?

Imagine wikipedia articles as a graph or web connected by links between each article.

It is important to note that links are one-way on wikipedia. An article links to an article but often isn't linked from that article.

The initial problem that this solves is measuring short distances between an article and itself on wikipedia. It does this in a brute force method, checking all nearby articles for links back to the TARGET_TITLE.

The fundamental 'useful thing' this does is cache internal links from wikipedia pages.  It can be extended to traverse the graph of wikipedia pages and "do stuff".

### How do I do it?

1. Put the Title of the page you want to start at in the ROOT_TITLE variable at the bottom.
2. Build the virtual environment and activate it.
3. Run `python traversal.py`
4. Tail the `debug.log` or sed/grep for only results.

