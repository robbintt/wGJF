
## Wikipedia Generalized Jesus Finder (wGJF)

A generalized tool to find references to an article by depth-searching internal wikipedia links.

Currently the search only finds references to the originating article, unless the TARGET_TITLE is altered.

Named after ["5 clicks to Jesus"](http://www.urbandictionary.com/define.php?term=5%20Clicks%20To%20Jesus).



### What the heck is this?

Wrote a recursive method for searching and added some logging. This doesn't store the resulting data anywhere. it should probably all be stored in a sqlite table. This could lighten the load on subsequent searches where 'recent information' could be reused.


### How do I do it?

1. Put the Title of the page you want to start at in the ROOT_TITLE variable at the bottom.
2. Build the virtual environment and activate it.
3. Run `python traversal.py`
4. Tail the `debug.log` or sed/grep for only results.

### What weird things are happening?

I needed to pip install requests security: $ pip install requests[security]
How can I get this into requirements.txt?
