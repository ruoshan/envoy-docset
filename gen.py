#!/usr/bin/env python3

import os, re, sqlite3, sys, fnmatch
from bs4 import BeautifulSoup, NavigableString, Tag

if len(sys.argv) != 2:
    print("gen.py {version}")
    sys.exit(1)
else:
    V = sys.argv[1]

db = sqlite3.connect('./docSet.dsidx')
cur = db.cursor()

try:
    cur.execute('DROP TABLE searchIndex;')
except:
    pass

cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = './Documents'


def list_all_target_files(dirname):
    rv = []
    for subdir, _, filenames in os.walk(dirname):
        rv.extend([os.path.join(subdir, f) for f in fnmatch.filter(filenames, "*.proto.html")])
    return rv

def gen_index(filename):
    print("processing %s" % filename)
    soup = BeautifulSoup(open(filename))

    for div in soup.find_all('div', {'class': "section"}):
        try:
            name = div.h2.text[:-1]
            path = filename[len(docpath) + 1:] + div.h2.a.attrs["href"]
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Type', path))
        except:
            continue

    for dl in soup.find_all("dl"):
        try:
            name = dl.dt.text
            path = filename[len(docpath) + 1:] + "#" + dl.attrs["id"]
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Option', path))
        except:
            continue


target_files = list_all_target_files(os.path.join(docpath, V, "api-v3")) # only index v3 keywords
for f in target_files:
    gen_index(f)

db.commit()
db.close()
