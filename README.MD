Wrote a recursive method for searching and added some logging. This doesn't store the resulting data anywhere. it should probably all be stored in a sqlite table. This could lighten the load on subsequent searches where 'recent information' could be reused.

Needed to pip install requests security: $ pip install requests[security]
How can I get this into requirements.txt?
