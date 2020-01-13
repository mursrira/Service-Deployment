# -*- mode: python; python-indent: 4 -*-
import re
import ncs
import inspect
import copy


class Helpers(object):
    def __init__(self, _self, tctx=None, service=None, root=None):
        self.log = _self.log
        if tctx is None:
            m = ncs.maapi.Maapi()
            m.start_user_session('admin', 'python')
            t = m.start_write_trans()
            root = ncs.maagic.get_root(t)
            self.th = t.th
            self.t = t
            self.my_maapi = ncs.maagic.get_maapi(root)
            self.log.info("Opening new transaction")
        else:
            self.tctx = tctx
            self.th = self.tctx.th
            self.my_maapi = ncs.maagic.get_maapi(service)

        self.service = service
        self.root = root
        self.my_maapi.attach(self.th)

