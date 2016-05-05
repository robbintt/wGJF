""" A little sample wiki robot for reading information

"""
import requests

TARGET_WIKI_URL = "https://en.wikipedia.org/w/api.php"

endpoint = dict()

# endpoint static setup
endpoint['action'] = 'query'
endpoint['format'] = 'json'
endpoint['titles'] = 'Main Page'
#endpoint['prop'] = 'revisions'
endpoint['rvprop'] = 'content'

headers = dict()
headers['user-agent'] = 'wiki-shallow-relation-graph/0.0.1'


if __name__ == "__main__":

    r = requests.get(TARGET_WIKI_URL, headers=headers, params=endpoint)

    if r.status_code == "200":

        entry_info = r.json()

        print(entry_info)

