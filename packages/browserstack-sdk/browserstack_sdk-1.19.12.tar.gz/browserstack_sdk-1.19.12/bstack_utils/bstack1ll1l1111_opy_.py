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
from collections import deque
from bstack_utils.constants import *
class bstack11l1l1ll_opy_:
    def __init__(self):
        self._1111ll11ll_opy_ = deque()
        self._1111l1ll1l_opy_ = {}
        self._1111l1l11l_opy_ = False
    def bstack1111l1lll1_opy_(self, test_name, bstack1111l1llll_opy_):
        bstack1111ll11l1_opy_ = self._1111l1ll1l_opy_.get(test_name, {})
        return bstack1111ll11l1_opy_.get(bstack1111l1llll_opy_, 0)
    def bstack1111l1ll11_opy_(self, test_name, bstack1111l1llll_opy_):
        bstack1111l11lll_opy_ = self.bstack1111l1lll1_opy_(test_name, bstack1111l1llll_opy_)
        self.bstack1111l11l1l_opy_(test_name, bstack1111l1llll_opy_)
        return bstack1111l11lll_opy_
    def bstack1111l11l1l_opy_(self, test_name, bstack1111l1llll_opy_):
        if test_name not in self._1111l1ll1l_opy_:
            self._1111l1ll1l_opy_[test_name] = {}
        bstack1111ll11l1_opy_ = self._1111l1ll1l_opy_[test_name]
        bstack1111l11lll_opy_ = bstack1111ll11l1_opy_.get(bstack1111l1llll_opy_, 0)
        bstack1111ll11l1_opy_[bstack1111l1llll_opy_] = bstack1111l11lll_opy_ + 1
    def bstack111ll1l11_opy_(self, bstack1111ll111l_opy_, bstack1111ll1111_opy_):
        bstack1111l1l1l1_opy_ = self.bstack1111l1ll11_opy_(bstack1111ll111l_opy_, bstack1111ll1111_opy_)
        bstack1111l11ll1_opy_ = bstack11ll111l1l_opy_[bstack1111ll1111_opy_]
        bstack1111l1l1ll_opy_ = bstack11lll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁ࠲ࢁࡽࠣᏒ").format(bstack1111ll111l_opy_, bstack1111l11ll1_opy_, bstack1111l1l1l1_opy_)
        self._1111ll11ll_opy_.append(bstack1111l1l1ll_opy_)
    def bstack1ll1l1l1l_opy_(self):
        return len(self._1111ll11ll_opy_) == 0
    def bstack11ll11lll_opy_(self):
        bstack1111l1l111_opy_ = self._1111ll11ll_opy_.popleft()
        return bstack1111l1l111_opy_
    def capturing(self):
        return self._1111l1l11l_opy_
    def bstack11lllll11_opy_(self):
        self._1111l1l11l_opy_ = True
    def bstack1111lllll_opy_(self):
        self._1111l1l11l_opy_ = False