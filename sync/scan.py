#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:expandtab

import binascii
import os

from Queue import Queue

from path import Path

def scan(path):
    paths = {}
    queue = Queue()
    queue.put('')
    while not queue.empty():
        subpath = queue.get()
        p = Path(os.path.join(path, subpath))
        paths[subpath] = p
        if p.path_type == Path.TYPE_DIRECTORY:
            for sp in p.content:
                queue.put(os.path.join(subpath, sp))

    state = sorted([(k, [binascii.hexlify(c.digest) for c in v.content]) for k,v in paths.items() if v.path_type == Path.TYPE_FILE])
    chunks = sum([v.content for k,v in paths.items() if v.path_type == Path.TYPE_FILE],list())
    
    return state, chunks

print scan('dw_sync')
