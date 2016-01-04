#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:expandtab

import binascii

import config

class Chunk:
    def __init__(self, digest=None, size=None, path=None, offset=None, data=None):
        self.digest = digest
        self.size = size
        self.path = path
        self.offset = offset
        self.data = data
        if data is not None:
            self.set_data(data)

    def __repr__(self):
        rep = []
        if self.digest is not None:
            rep.append('#' + binascii.hexlify(self.digest))
        rep.append(':'.join([str(p) for p in [self.path, self.offset, self.size] if p is not None]))
        if self.data is not None:
            rep.append(binascii.hexlify(self.data))
        return 'Chunk('+', '.join([repr(r) for r in rep if r])+')'

    def set_data(self, data):
        self.data = data
        if self.data is not None:
            data_size = len(self.data)
            data_digest = config.CHUNK_DIGEST(self.data)
            if self.digest is not None and self.digest != data_digest:
                raise RuntimeError('Chunk digest mismatch')
            if self.size is not None and self.size != data_size:
                raise RuntimeError('Chunk size mismatch')
            self.digest = data_digest
            self.size = data_size

    def get_data(self):
        if self.data is not None:
            return self.data
        if self.digest is not None and self.size is not None and self.path is not None and self.offset is not None:
            with open(self.path, 'rb') as fd:
                fd.seek(self.offset)
                data = fd.read(self.size)
            self.update(data)
        else:
            raise RuntimeError('Chunk unknown')
    
    def forget_data(self):
        if self.data is not None and self.size is not None and self.path is not None and self.offset is not None:
            self.data = None
