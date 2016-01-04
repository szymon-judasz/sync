#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:expandtab

import binascii
import errno
import os

import config
from chunk import Chunk

class Path:
    TYPE_NONEXISTENT = 0
    TYPE_DIRECTORY   = 1
    TYPE_FILE        = 2
    TYPE_LINK        = 3
    TYPE_UNKNOWN     = 4

    def __init__(self, path, read_chunks=True):
        self.path = path
        if not os.path.exists(self.path):
            self.path_type = Path.TYPE_NONEXISTENT
        else:
            try:
                if os.path.islink(self.path):
                    self.path_type = Path.TYPE_LINK
                    self.content = os.readlink(self.path)
                elif os.path.isdir(self.path):
                    self.path_type = Path.TYPE_DIRECTORY
                    self.content = sorted(os.listdir(self.path))
                elif os.path.isfile(self.path):
                    self.path_type = Path.TYPE_FILE
                    self.content = None
                else:
                    self.path_type = Path.TYPE_UNKNOWN
                    return
                stats = os.lstat(self.path)
                self.mode = stats.st_mode
                self.mtime = stats.st_mtime
                self.ctime = stats.st_ctime
                if self.path_type == Path.TYPE_FILE:
                    self.size = stats.st_size
                    if read_chunks:
                        self.read_chunks()
            except OSError as exc:
                if exc.errno == errno.EEXIST:
                    self.path_type = Path.TYPE_NONEXISTENT
                else:
                    raise

    def read_chunks(self):
        self.content = list()
        offset = 0
        with open(self.path, 'rb') as fd:
            while True:
                data = fd.read(config.CHUNK_SIZE)
                if data is None or len(data) == 0:
                    break
                self.content.append(Chunk(path=self.path, offset=offset, data=data))
                offset += len(data)

    def changed(self, path):
        current = Path(self.path, read_chunks=False)
        return self != current

    def __eq__(self, other):
        if self.path_type != other.path_type:
            return False
        if self.path_type == Path.TYPE_NONEXISTENT:
            return True
        if self.mode != other.mode:
            return False
        if self.mtime != other.mtime:
            return False
        if self.ctime != other.ctime:
            return False
        if self.path_type == Path.TYPE_LINK:
            return self.content == other.content
        if self.path_type == Path.TYPE_DIRECTORY:
            return self.content == other.content
        if self.path_type == Path.TYPE_FILE:
            if self.content is not None and other.content is not None:
                return self.content == other.content
            return self.size == other.size
        return True
    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def digest(self):
        desc = list()
        desc.append(self.path_type)
        if self.path_type != Path.TYPE_NONEXISTENT:
            if self.path_type == Path.TYPE_LINK:
                desc.append(self.content)
            elif self.path_type == Path.TYPE_DIRECTORY:
                desc.append('*'.join(self.content))
            elif self.path_type == Path.TYPE_FILE:
                desc.append('*'.join([binascii.hexlify(c.digest) for c in self.content]))
                desc.append(self.size)
            desc.append(self.mode)
            desc.append(self.mtime)
            desc.append(self.ctime)
        return config.PATH_DIGEST('|'.join([str(d) for d in desc]))

    def __repr__(self):
        rep = []
        rep.append(self.path_type)
        if self.path_type != Path.TYPE_NONEXISTENT:
            rep.append(self.mode)
            rep.append(self.mtime)
            rep.append(self.ctime)
            rep.append(self.content)
            rep.append('#' + binascii.hexlify(self.digest))
        return 'Path('+', '.join([repr(r) for r in rep if r])+')'
