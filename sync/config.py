#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:expandtab

import hashlib

CHUNK_SIZE = 65536
CHUNK_DIGEST = lambda b : hashlib.sha1(b).digest()
PATH_DIGEST = CHUNK_DIGEST
