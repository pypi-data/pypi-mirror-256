# coding: UTF-8
import sys
bstack111l11l_opy_ = sys.version_info [0] == 2
bstack1111lll_opy_ = 2048
bstack1111ll_opy_ = 7
def bstack11lll_opy_ (bstack1l1l_opy_):
    global bstack1ll_opy_
    bstack1111l1l_opy_ = ord (bstack1l1l_opy_ [-1])
    bstack1111l1_opy_ = bstack1l1l_opy_ [:-1]
    bstack1ll1_opy_ = bstack1111l1l_opy_ % len (bstack1111l1_opy_)
    bstack111l11_opy_ = bstack1111l1_opy_ [:bstack1ll1_opy_] + bstack1111l1_opy_ [bstack1ll1_opy_:]
    if bstack111l11l_opy_:
        bstack11lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1111lll_opy_ - (bstack1l1l1_opy_ + bstack1111l1l_opy_) % bstack1111ll_opy_) for bstack1l1l1_opy_, char in enumerate (bstack111l11_opy_)])
    else:
        bstack11lll1l_opy_ = str () .join ([chr (ord (char) - bstack1111lll_opy_ - (bstack1l1l1_opy_ + bstack1111l1l_opy_) % bstack1111ll_opy_) for bstack1l1l1_opy_, char in enumerate (bstack111l11_opy_)])
    return eval (bstack11lll1l_opy_)
import threading
bstack111111l1l1_opy_ = 1000
bstack111111llll_opy_ = 5
bstack111111l111_opy_ = 30
bstack111111ll11_opy_ = 2
class bstack1111111l1l_opy_:
    def __init__(self, handler, bstack1111111l11_opy_=bstack111111l1l1_opy_, bstack1111111lll_opy_=bstack111111llll_opy_):
        self.queue = []
        self.handler = handler
        self.bstack1111111l11_opy_ = bstack1111111l11_opy_
        self.bstack1111111lll_opy_ = bstack1111111lll_opy_
        self.lock = threading.Lock()
        self.timer = None
    def start(self):
        if not self.timer:
            self.bstack111111ll1l_opy_()
    def bstack111111ll1l_opy_(self):
        self.timer = threading.Timer(self.bstack1111111lll_opy_, self.bstack111111lll1_opy_)
        self.timer.start()
    def bstack1111111ll1_opy_(self):
        self.timer.cancel()
    def bstack111111l1ll_opy_(self):
        self.bstack1111111ll1_opy_()
        self.bstack111111ll1l_opy_()
    def add(self, event):
        with self.lock:
            self.queue.append(event)
            if len(self.queue) >= self.bstack1111111l11_opy_:
                t = threading.Thread(target=self.bstack111111lll1_opy_)
                t.start()
                self.bstack111111l1ll_opy_()
    def bstack111111lll1_opy_(self):
        if len(self.queue) <= 0:
            return
        data = self.queue[:self.bstack1111111l11_opy_]
        del self.queue[:self.bstack1111111l11_opy_]
        self.handler(data)
    def shutdown(self):
        self.bstack1111111ll1_opy_()
        while len(self.queue) > 0:
            self.bstack111111lll1_opy_()